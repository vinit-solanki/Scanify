import os
import logging
from typing import Dict

logger = logging.getLogger(__name__)


def _rule_based_explanation(ctx: Dict, mode: str) -> str:
    """Generate explanation without LLM using simple rules."""
    ing = ctx.get("ingredients") or []
    nutr_per_100g = ctx.get("nutrition_per_100g") or ctx.get("nutrition") or {}
    recommendations = ctx.get("risks") or ctx.get("recommendations") or []
    score = ctx.get("score", 50)
    category = ctx.get("health_category", "Unknown")
    
    lines = []
    
    # Header
    lines.append(f"**Health Analysis: {category}** | Score: {score}/100")
    
    # Key ingredients summary
    if ing:
        ing_preview = ", ".join(ing[:5])
        if len(ing) > 5:
            ing_preview += f", and {len(ing)-5} more"
        lines.append(f"\n**Key Ingredients:** {ing_preview}")
    
    # Nutrition summary
    nutr_items = []
    if nutr_per_100g.get("calories"):
        nutr_items.append(f"Calories: {nutr_per_100g.get('calories')} kcal")
    if nutr_per_100g.get("protein_g"):
        nutr_items.append(f"Protein: {nutr_per_100g.get('protein_g')}g")
    if nutr_per_100g.get("sugars_g"):
        nutr_items.append(f"Sugars: {nutr_per_100g.get('sugars_g')}g")
    if nutr_per_100g.get("dietary_fiber_g"):
        nutr_items.append(f"Fiber: {nutr_per_100g.get('dietary_fiber_g')}g")
    
    if nutr_items:
        lines.append(f"\n**Nutrition (per 100g):** {' | '.join(nutr_items)}")
    
    # Recommendations
    if recommendations:
        lines.append(f"\n**Recommendations:**")
        for rec in recommendations:
            if isinstance(rec, dict):
                lines.append(f"• {rec.get('reason', rec)}")
            else:
                lines.append(f"• {rec}")
    
    # Mode-specific advice
    if mode == "diabetes":
        lines.append("\n**Diabetes-Focused Advice:** Focus on limiting sugar and refined carbohydrates. Choose products with more fiber and whole grains.")
    elif mode == "weight_loss":
        lines.append("\n**Weight Loss Advice:** Consider calorie intake and nutrient density. Prioritize high-protein, high-fiber options for better satiety.")
    
    return "\n".join(lines)


def generate_explanation(ctx: Dict, mode: str) -> str:
    """
    Generate a detailed explanation of the analysis.
    Attempts to use Gemini API if available, falls back to rule-based explanation.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    # If no API key, use rule-based explanation
    if not api_key:
        logger.info("GEMINI_API_KEY not configured, using rule-based explanation")
        return _rule_based_explanation(ctx, mode)
    
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        
        # Prepare context for LLM
        ing = ctx.get("ingredients") or []
        nutr = ctx.get("nutrition_per_100g") or {}
        allergens = ctx.get("allergens") or []
        additives = ctx.get("additives") or []
        recommendations = ctx.get("recommendations") or []
        score = ctx.get("score", 0)
        
        prompt = f"""You are a nutrition assistant. Analyze this food product and provide a concise, helpful explanation.

Product Mode: {mode.upper()}
Health Score: {score}/100

Ingredients: {', '.join(ing) if ing else 'Not extracted'}
Allergens: {', '.join(allergens) if allergens else 'None detected'}
Additives: {', '.join(additives) if additives else 'None detected'}

Nutrition per 100g:
- Calories: {nutr.get('calories', 'N/A')}
- Protein: {nutr.get('protein_g', 'N/A')}g
- Sugars: {nutr.get('sugars_g', 'N/A')}g
- Fiber: {nutr.get('dietary_fiber_g', 'N/A')}g
- Fat: {nutr.get('fat_g', 'N/A')}g
- Saturated Fat: {nutr.get('saturated_fat_g', 'N/A')}g

Key Concerns: {'; '.join(recommendations) if recommendations else 'None'}

Provide a brief, factual explanation (2-3 sentences) of the nutritional quality for the {mode} mode, citing actual values. Then give 1-2 actionable recommendations. Be concise and helpful."""
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt, timeout=10)
        
        explanation = getattr(response, "text", None)
        if explanation:
            logger.info("Generated explanation with Gemini")
            return explanation
        else:
            logger.warning("Gemini returned empty response")
            return _rule_based_explanation(ctx, mode)
    
    except Exception as e:
        logger.warning(f"Error calling Gemini API: {str(e)}, using rule-based explanation")
        return _rule_based_explanation(ctx, mode)
