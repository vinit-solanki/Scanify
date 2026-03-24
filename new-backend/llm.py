import os
import logging
import time
from typing import Dict, Any

import httpx

logger = logging.getLogger(__name__)

OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_TIMEOUT_SECONDS = max(int(os.getenv("OPENROUTER_TIMEOUT_SECONDS", "15")), 1)
OPENROUTER_QUOTA_COOLDOWN_SECONDS = max(int(os.getenv("OPENROUTER_QUOTA_COOLDOWN_SECONDS", "120")), 1)
OPENROUTER_SITE_URL = (os.getenv("OPENROUTER_SITE_URL") or "").strip()
OPENROUTER_SITE_NAME = (os.getenv("OPENROUTER_SITE_NAME") or "Scanify").strip()

_openrouter_cooldown_until = 0.0


def _fmt_num(value: Any, suffix: str = "") -> str:
    try:
        if value is None or value == "N/A":
            return "N/A"
        num = float(value)
        if num.is_integer():
            return f"{int(num)}{suffix}"
        return f"{num:.1f}{suffix}"
    except Exception:
        return f"{value}{suffix}" if value is not None else "N/A"


def _mode_label(mode: str) -> str:
    if mode == "weight_loss":
        return "Weight Loss"
    if mode == "diabetes":
        return "Diabetes"
    return "General"


def _build_prompt(ctx: Dict, mode: str) -> str:
    ing = ctx.get("ingredients") or []
    nutr = ctx.get("nutrition_per_100g") or {}
    allergens = ctx.get("allergens") or []
    additives = ctx.get("additives") or []
    recommendations = ctx.get("recommendations") or []
    penalties = ctx.get("penalties") or {}
    score = _fmt_num(ctx.get("score", 0))
    category = ctx.get("health_category", "Unknown")
    serving_desc = ctx.get("serving_size_description") or "Not extracted"

    return f"""You are a nutrition assistant for packaged food labels.

Use ONLY the provided values. Do not invent missing values. Do not provide diagnosis, treatment, or medical guarantees.

Product Mode: {_mode_label(mode)}
Health Score: {score}/100
Health Category: {category}
Serving Size: {serving_desc}

Ingredients: {', '.join(ing) if ing else 'Not extracted'}
Allergens: {', '.join(allergens) if allergens else 'None detected'}
Additives: {', '.join(additives) if additives else 'None detected'}

Nutrition per 100g:
- Calories: {_fmt_num(nutr.get('calories'))} kcal
- Protein: {_fmt_num(nutr.get('protein_g'), 'g')}
- Sugars: {_fmt_num(nutr.get('sugars_g'), 'g')}
- Fiber: {_fmt_num(nutr.get('dietary_fiber_g'), 'g')}
- Fat: {_fmt_num(nutr.get('total_fat_g', nutr.get('fat_g')), 'g')}
- Saturated Fat: {_fmt_num(nutr.get('saturated_fat_g'), 'g')}
- Sodium: {_fmt_num(nutr.get('sodium_mg'), 'mg')}

Scoring Concerns: {'; '.join(recommendations) if recommendations else 'None'}
Penalty Flags: {', '.join(sorted(penalties.keys())) if penalties else 'None'}

Return markdown in EXACTLY this structure:

## Summary
Start with one decision phrase in the first sentence: "Best for regular use", "Okay occasionally", or "Limit/Avoid".
Then write 2-4 sentences explaining overall nutritional quality for the selected mode using concrete values.

## Key Positives
- 2-4 bullets with numeric evidence where available.

## Key Concerns
- 2-4 bullets with numeric evidence where available.

## Recommendations
- 3 specific, practical actions tied to the above concerns.

## Confidence Note
One short sentence describing uncertainty from missing values/OCR limits.

Hard constraints:
- Keep the judgment mode-specific. Do not reuse identical wording across different modes.
- If sugars/carbs are high, emphasize diabetes risk.
- If calories/fat are high, emphasize weight-loss risk.
- If data is missing, explicitly say what is missing.
"""


def _rule_based_explanation(ctx: Dict, mode: str) -> str:
    """Generate structured explanation without LLM using deterministic rules."""
    ing = ctx.get("ingredients") or []
    nutr_per_100g = ctx.get("nutrition_per_100g") or ctx.get("nutrition") or {}
    recommendations = ctx.get("risks") or ctx.get("recommendations") or []
    score = ctx.get("score", 50)
    category = ctx.get("health_category", "Unknown")

    decision = "Okay occasionally"
    if isinstance(score, (int, float)):
        if score >= 80:
            decision = "Best for regular use"
        elif score < 50:
            decision = "Limit/Avoid"

    calories = nutr_per_100g.get("calories")
    protein = nutr_per_100g.get("protein_g")
    sugar = nutr_per_100g.get("sugars_g")
    fiber = nutr_per_100g.get("dietary_fiber_g")
    fat = nutr_per_100g.get("total_fat_g", nutr_per_100g.get("fat_g"))
    sodium = nutr_per_100g.get("sodium_mg")

    positives = []
    concerns = []

    if protein is not None and float(protein) >= 10:
        positives.append(f"Protein is relatively strong at {_fmt_num(protein, 'g')} per 100g.")
    if fiber is not None and float(fiber) >= 5:
        positives.append(f"Fiber is supportive at {_fmt_num(fiber, 'g')} per 100g.")
    if sugar is not None and float(sugar) <= 5:
        positives.append(f"Sugar is on the lower side at {_fmt_num(sugar, 'g')} per 100g.")

    if calories is not None and float(calories) > 250:
        concerns.append(f"Calories are elevated at {_fmt_num(calories)} kcal per 100g.")
    if sugar is not None and float(sugar) > 10:
        concerns.append(f"Sugar is relatively high at {_fmt_num(sugar, 'g')} per 100g.")
    if fat is not None and float(fat) > 15:
        concerns.append(f"Fat is relatively high at {_fmt_num(fat, 'g')} per 100g.")
    if sodium is not None and float(sodium) > 600:
        concerns.append(f"Sodium is high at {_fmt_num(sodium, 'mg')} per 100g.")

    if not positives:
        positives.append("Nutritional profile has some useful components, but data is limited.")
    if not concerns:
        concerns.append("No major red flags were detected from the extracted values.")

    ing_preview = ", ".join(ing[:8]) if ing else "Not extracted"
    if len(ing) > 8:
        ing_preview += f", and {len(ing)-8} more"

    rec_lines = []
    for rec in recommendations[:3]:
        if isinstance(rec, dict):
            rec_lines.append(f"- {rec.get('reason', str(rec))}")
        else:
            rec_lines.append(f"- {rec}")

    if len(rec_lines) < 3:
        if mode == "diabetes":
            rec_lines.extend([
                "- Prefer options with lower sugar and lower refined carbohydrate content.",
                "- Pair with high-fiber foods to improve glycemic response.",
            ])
        elif mode == "weight_loss":
            rec_lines.extend([
                "- Prioritize options with higher protein and fiber for satiety.",
                "- Keep portions moderate if calories are high per 100g.",
            ])
        else:
            rec_lines.extend([
                "- Compare with similar products and choose lower sugar/sodium options.",
                "- Prefer shorter ingredient lists with fewer additives.",
            ])
    rec_lines = rec_lines[:3]

    lines = [
        "## Summary",
        f"{decision}: this product is rated **{category}** with a health score of **{_fmt_num(score)}/100** for **{_mode_label(mode)}** mode.",
        f"Key extracted ingredients include: {ing_preview}.",
        f"Per 100g snapshot: calories {_fmt_num(calories)}, protein {_fmt_num(protein, 'g')}, sugars {_fmt_num(sugar, 'g')}, fiber {_fmt_num(fiber, 'g')}, fat {_fmt_num(fat, 'g')}.",
        "",
        "## Key Positives",
        *[f"- {item}" for item in positives[:4]],
        "",
        "## Key Concerns",
        *[f"- {item}" for item in concerns[:4]],
        "",
        "## Recommendations",
        *rec_lines,
        "",
        "## Confidence Note",
        "This explanation is based on OCR/parsing output; missing or unclear label fields can reduce precision.",
    ]

    return "\n".join(lines)


def generate_explanation(ctx: Dict, mode: str) -> str:
    """
    Generate a detailed explanation of the analysis.
    Attempts to use OpenRouter API if available, falls back to rule-based explanation.
    """
    global _openrouter_cooldown_until
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    # If no API key, use rule-based explanation
    if not api_key:
        logger.info("OPENROUTER_API_KEY not configured, using rule-based explanation")
        return _rule_based_explanation(ctx, mode)

    if time.time() < _openrouter_cooldown_until:
        logger.info("OpenRouter temporarily disabled due to recent quota exhaustion; using rule-based explanation")
        return _rule_based_explanation(ctx, mode)

    prompt = _build_prompt(ctx, mode)
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        if OPENROUTER_SITE_URL:
            headers["HTTP-Referer"] = OPENROUTER_SITE_URL
        if OPENROUTER_SITE_NAME:
            headers["X-Title"] = OPENROUTER_SITE_NAME

        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a nutrition assistant. Be factual, concise, and avoid diagnosis/treatment claims.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": 0.3,
            "max_tokens": 420,
        }

        response = httpx.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=OPENROUTER_TIMEOUT_SECONDS,
        )

        if response.status_code == 429:
            _openrouter_cooldown_until = time.time() + OPENROUTER_QUOTA_COOLDOWN_SECONDS
            logger.warning("OpenRouter quota/rate limit exceeded; using rule-based explanation")
            return _rule_based_explanation(ctx, mode)

        response.raise_for_status()
        data = response.json()
        explanation = data.get("choices", [{}])[0].get("message", {}).get("content")

        if explanation:
            logger.info("Generated explanation with OpenRouter")
            return explanation.strip()

        logger.warning("OpenRouter returned empty response")
    except Exception as e:
        logger.warning("OpenRouter call failed: %s", str(e))

    return _rule_based_explanation(ctx, mode)
