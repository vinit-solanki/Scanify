import cv2
import numpy as np

def preprocess_image(image_path):
    """
    Preprocess image to improve OCR accuracy.
    Handles skew, contrast, noise, and resolution.
    """

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Invalid image path")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Resize (important for small text)
    scale_factor = 2
    gray = cv2.resize(
        gray,
        None,
        fx=scale_factor,
        fy=scale_factor,
        interpolation=cv2.INTER_CUBIC
    )

    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        2
    )

    # Noise removal
    kernel = np.ones((1, 1), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    return cleaned
