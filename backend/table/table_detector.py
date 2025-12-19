from text_utils.text_utils import normalize_text

NUTRITION_KEYWORDS = [
    "energy", "calories", "fat", "protein",
    "carbohydrate", "sugar", "sodium"
]

def detect_nutrition_blocks(blocks):
    detected = []

    for b in blocks:
        text = normalize_text(b["text"])
        if any(k in text for k in NUTRITION_KEYWORDS):
            detected.append(b)

    return detected
