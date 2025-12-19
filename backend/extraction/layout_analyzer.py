from text_utils.text_utils import normalize_text

INGREDIENT_ANCHORS = ["ingredients", "contains"]
NUTRITION_ANCHORS = [
    "nutrition", "nutrition facts", "calories", "energy"
]

def analyze_layout(text_blocks):
    """
    Identifies semantic regions of the label.
    Returns blocks grouped by region.
    """

    ingredient_blocks = []
    nutrition_blocks = []
    other_blocks = []

    for block in text_blocks:
        text = normalize_text(block["text"])

        if any(anchor in text for anchor in INGREDIENT_ANCHORS):
            ingredient_blocks.append(block)
        elif any(anchor in text for anchor in NUTRITION_ANCHORS):
            nutrition_blocks.append(block)
        else:
            other_blocks.append(block)

    return {
        "ingredient_blocks": expand_region(ingredient_blocks, text_blocks),
        "nutrition_blocks": expand_region(nutrition_blocks, text_blocks),
        "other_blocks": other_blocks
    }


def expand_region(anchor_blocks, all_blocks, y_margin=120):
    """
    Expands a region vertically around anchor blocks
    to capture related text.
    """

    if not anchor_blocks:
        return []

    y_positions = [b["bbox"]["y"] for b in anchor_blocks]
    min_y = min(y_positions) - y_margin
    max_y = max(y_positions) + y_margin

    region_blocks = [
        b for b in all_blocks
        if min_y <= b["bbox"]["y"] <= max_y
    ]

    return region_blocks
