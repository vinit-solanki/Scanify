from text_utils.text_utils import normalize_text

def extract_ingredients(ingredient_blocks):
    """
    Extracts and cleans ingredient list text.
    """

    if not ingredient_blocks:
        return {
            "raw_text": "",
            "ingredients": [],
            "confidence": 0
        }

    sorted_blocks = sorted(
        ingredient_blocks,
        key=lambda b: (b["bbox"]["y"], b["bbox"]["x"])
    )

    combined_text = " ".join(
        normalize_text(b["text"]) for b in sorted_blocks
    )

    # Remove header words
    for h in ["ingredients", "contains"]:
        combined_text = combined_text.replace(h, "")

    ingredients = [
        ing.strip()
        for ing in combined_text.split(",")
        if len(ing.strip()) > 2
    ]

    avg_confidence = (
        sum(b["confidence"] for b in ingredient_blocks) /
        len(ingredient_blocks)
    )

    return {
        "raw_text": combined_text,
        "ingredients": ingredients,
        "confidence": round(avg_confidence, 2)
    }
