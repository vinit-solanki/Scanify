import pytesseract
import os
from pytesseract import Output
from vision.image_preprocessor import preprocess_image

# Set Tesseract path from environment or use defaults for Windows/Linux
tesseract_path = os.getenv("TESSERACT_PATH")
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    # Default paths for Windows
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

# Set TESSDATA_PREFIX from environment or use default
tessdata_prefix = os.getenv("TESSDATA_PREFIX")
if tessdata_prefix:
    os.environ["TESSDATA_PREFIX"] = tessdata_prefix
else:
    # Default path for Windows
    os.environ["TESSDATA_PREFIX"] = (
        r"C:\Program Files\Tesseract-OCR\tessdata"
    )

def extract_text_blocks(image_path):
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
        conf = int(ocr_data["conf"][i])

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
