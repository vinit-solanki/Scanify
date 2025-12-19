import pytesseract
import os
from pytesseract import Output
from vision.image_preprocessor import preprocess_image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

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
