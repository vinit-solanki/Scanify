import os
import pytesseract
from pytesseract import Output
from vision.image_preprocessor import preprocess_image


def configure_tesseract():
    """
    Configure Tesseract path and tessdata directory.
    Windows default: C:\\Program Files\\Tesseract-OCR\\
    Linux/Docker default: /usr/bin/tesseract
    """
    tesseract_path = os.getenv("TESSERACT_PATH")
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path


configure_tesseract()


def extract_text_blocks(image_path):
    """
    Extract OCR text blocks with bounding boxes and confidence scores using Tesseract.
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
        except (ValueError, IndexError):
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

