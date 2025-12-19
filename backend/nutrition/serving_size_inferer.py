import re

DEFAULT_SERVING_G = 30  # industry prior

def infer_serving_size(text_blocks):
    """
    Attempts to infer serving size from OCR text.
    Falls back to industry priors if missing.
    """

    combined_text = " ".join(b["text"].lower() for b in text_blocks)

    match = re.search(r"serving size\s*[:\-]?\s*(\d+)\s*g", combined_text)
    if match:
        return int(match.group(1)), 0.95

    match = re.search(r"per\s*(\d+)\s*g", combined_text)
    if match:
        return int(match.group(1)), 0.85

    return DEFAULT_SERVING_G, 0.6
