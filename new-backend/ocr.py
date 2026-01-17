import io
from typing import Optional
from PIL import Image, ImageOps, ImageFilter

try:
    import pytesseract
except Exception:  # pragma: no cover
    pytesseract = None


def extract_text(image_bytes: bytes) -> str:
    """Basic OCR over the whole image using Tesseract.
    Returns plain text; gracefully degrades to empty string if OCR unavailable.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("L")
        image = ImageOps.autocontrast(image)
        image = image.filter(ImageFilter.SHARPEN)
        if pytesseract is None:
            return ""
        text = pytesseract.image_to_string(image, lang="eng")
        return text if isinstance(text, str) else ""
    except Exception:
        return ""
