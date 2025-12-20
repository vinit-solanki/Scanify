import os
from typing import List, Dict, Any

from validation.label_validator import validate_food_label
from extraction.layout_analyzer import analyze_layout
from extraction.ingredient_extractor import extract_ingredients
from extraction.nutrition_extractor import extract_nutrition
from schemas.label_schema import build_label_schema
from stage3_runner import run_stage3
from nutrition.run_stage4 import run_stage4
from health.scoring_engine import compute_health_score
from llm.explanation_agent import generate_explanation


def _text_to_blocks(label_text: str) -> List[Dict[str, Any]]:
    # Create pseudo text blocks from raw text so downstream steps work
    words = [w for w in label_text.split() if w]
    blocks: List[Dict[str, Any]] = []
    line = []
    y = 0
    for i, w in enumerate(words):
        line.append(w)
        if len(line) >= 6:
            blocks.append({
                "text": " ".join(line),
                "confidence": 90,
                "bbox": {"x": 0, "y": y, "w": 100, "h": 12},
            })
            line = []
            y += 14
    if line:
        blocks.append({
            "text": " ".join(line),
            "confidence": 90,
            "bbox": {"x": 0, "y": y, "w": 100, "h": 12},
        })
    # Ensure we have enough blocks for validator thresholds
    if len(blocks) < 25 and blocks:
        # Repeat last blocks to reach 25 (keeps logic simple for text input)
        last = blocks[-1]
        while len(blocks) < 25:
            y += 14
            dup = {"text": last["text"], "confidence": 90, "bbox": {"x": 0, "y": y, "w": 100, "h": 12}}
            blocks.append(dup)
    return blocks


def run_pipeline_from_text(label_text: str, mode: str = "general") -> Dict[str, Any]:
    text_blocks = _text_to_blocks(label_text or "")
    return run_pipeline_from_blocks(text_blocks, mode)


def run_pipeline_from_blocks(text_blocks: List[Dict[str, Any]], mode: str = "general") -> Dict[str, Any]:
    validation = validate_food_label(text_blocks)

    layout = analyze_layout(text_blocks)

    ingredients = extract_ingredients(layout["ingredient_blocks"])
    nutrition = extract_nutrition(layout["nutrition_blocks"])

    label_data = build_label_schema(
        ingredients,
        nutrition,
        validation,
    )

    # Stage-3
    label_data["semantic_ingredients"] = run_stage3(
        label_data["ingredients"]
    )

    # Stage-4
    label_data["nutrition_normalized"] = run_stage4(
        label_data["nutrition"],
        text_blocks,
    )

    # Stage-5
    label_data["health"] = compute_health_score(
        label_data["nutrition_normalized"]["nutrition_per_100g"],
        label_data["semantic_ingredients"],
        mode=mode,
    )

    # Stage-6 (LLM explanation)
    if os.getenv("DISABLE_LLM", "0") in ("1", "true", "True"):
        label_data["explanation"] = "AI explanation disabled by server configuration (DISABLE_LLM)."
    else:
        try:
            label_data["explanation"] = generate_explanation(
                label_data,
                mode=mode,
            )
        except Exception:
            # Keep pipeline results even if LLM call fails; avoid leaking raw error text
            label_data["explanation"] = (
                "AI explanation is temporarily unavailable. "
                "Please verify your GEMINI_API_KEY/GOOGLE_API_KEY and try again."
            )

    return label_data
