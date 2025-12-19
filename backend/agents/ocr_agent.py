import pytesseract
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()

pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH")

def extract_text_from_image(image_path):
    """
    Performs OCR on label image
    """
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang="eng")

    return text.strip()
