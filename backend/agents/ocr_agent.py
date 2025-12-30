"""OCR wrapper that delegates to Google Document AI blocks."""

from vision.ocr_agent import extract_text_blocks


def extract_text_from_image(image_path: str) -> str:
    blocks = extract_text_blocks(image_path)
    return "\n".join([b.get("text", "") for b in blocks]).strip()
