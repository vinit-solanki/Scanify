import os
import platform
import pytesseract
from pytesseract import Output
from vision.image_preprocessor import preprocess_image


def configure_tesseract():
    """
    Configure Tesseract path and tessdata directory
    for Windows (local) and Linux (Render/Docker).
    Environment variables take highest priority.
    """

    # 1️⃣ Explicit override via environment variable
    tesseract_path = os.getenv("TESSERACT_PATH")
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
    else:
        system = platform.system().lower()

        # 2️⃣ Linux (Render, Docker, servers)
        if system == "linux":
            pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
            os.environ.setdefault(
                "TESSDATA_PREFIX",
                "/usr/share/tesseract-ocr/5/tessdata"
            )

        # 3️⃣ Windows (local development)
        elif system == "windows":
            pytesseract.pytesseract.tesseract_cmd = (
                r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            )
            os.environ.setdefault(
                "TESSDATA_PREFIX",
                r"C:\Program Files\Tesseract-OCR\tessdata"
            )

    # 4️⃣ Fail fast if Tesseract is still missing
    if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
        raise RuntimeError(
            f"Tesseract binary not found at: {pytesseract.pytesseract.tesseract_cmd}"
        )


# Configure once at import time
configure_tesseract()


def extract_text_blocks(image_path):
    """
    Extract OCR text blocks with bounding boxes and confidence scores.
    """

    processed_image = preprocess_image(image_path)

    ocr_data = pytesseract.image_to_data(
        processed_image,
        output_type=Output.DICT,
        config="--psm 6 -l eng"
    )

    text_blocks = []
    n = len(ocr_data["text"])

    for i in range(n):
        text = ocr_data["text"][i].strip()

        try:
            conf = int(float(ocr_data["conf"][i]))
        except ValueError:
            continue

        if text and conf > 40:
            text_blocks.append({
                "text": text,
                "confidence": conf,
                "bbox": {
                    "x": ocr_data["left"][i],
                    "y": ocr_data["top"][i],
                    "w": ocr_data["width"][i],
                    "h": ocr_data["height"][i],
                }
            })

    return text_blocks
