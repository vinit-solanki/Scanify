def validate_ocr_text(text):
    """
    Validates if OCR text is sufficient for analysis
    """

    if not text or len(text) < 50:
        return {
            "is_valid": False,
            "reason": "Text too short or unreadable"
        }

    keywords = ["ingredient", "nutrition", "energy", "fat", "protein", "sugar"]
    found = any(word.lower() in text.lower() for word in keywords)

    if not found:
        return {
            "is_valid": False,
            "reason": "Nutritional keywords not detected"
        }

    return {
        "is_valid": True
    }
