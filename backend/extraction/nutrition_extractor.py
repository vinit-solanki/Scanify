import re
from text_utils.text_utils import normalize_text

NUTRIENT_PATTERNS = {
    "calories": r"calories\s*(\d+)",
    "total_fat": r"total fat\s*(\d+\.?\d*)\s*g",
    "saturated_fat": r"saturated fat\s*(\d+\.?\d*)\s*g",
    "sodium": r"sodium\s*(\d+)\s*mg",
    "carbohydrate": r"total carbohydrate\s*(\d+\.?\d*)\s*g",
    "sugars": r"total sugars\s*(\d+\.?\d*)\s*g",
    "protein": r"protein\s*(\d+\.?\d*)\s*g",
}

def extract_nutrition(nutrition_blocks):
    """
    Parses nutrition facts from table-like text.
    """

    combined_text = " ".join(
        normalize_text(b["text"]) for b in nutrition_blocks
    )

    nutrition_data = {}

    for nutrient, pattern in NUTRIENT_PATTERNS.items():
        match = re.search(pattern, combined_text)
        if match:
            nutrition_data[nutrient] = match.group(1)
        else:
            nutrition_data[nutrient] = None

    avg_confidence = (
        sum(b["confidence"] for b in nutrition_blocks) /
        len(nutrition_blocks)
        if nutrition_blocks else 0
    )

    return {
        "nutrition": nutrition_data,
        "confidence": round(avg_confidence, 2)
    }
