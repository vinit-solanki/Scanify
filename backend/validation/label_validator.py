from text_utils.text_utils import normalize_text

REQUIRED_SIGNALS = {
    "nutrition": ["nutrition", "calories", "fat", "protein", "carbohydrate"],
    "ingredients": ["ingredients", "contains"],
    "units": ["g", "mg", "%"]
}

def validate_food_label(text_blocks):
    """
    Determines whether the image is a valid food label.
    Returns a structured validation report.
    """

    combined_text = " ".join(
        normalize_text(block["text"]) for block in text_blocks
    )

    signal_score = 0
    missing_signals = []

    for signal, keywords in REQUIRED_SIGNALS.items():
        if any(keyword in combined_text for keyword in keywords):
            signal_score += 1
        else:
            missing_signals.append(signal)

    avg_confidence = (
        sum(block["confidence"] for block in text_blocks) / len(text_blocks)
        if text_blocks else 0
    )

    is_valid = (
        signal_score >= 2 and
        avg_confidence >= 55 and
        len(text_blocks) >= 25
    )

    return {
        "is_valid_label": is_valid,
        "signal_score": signal_score,
        "missing_signals": missing_signals,
        "average_ocr_confidence": round(avg_confidence, 2),
        "num_text_blocks": len(text_blocks)
    }
