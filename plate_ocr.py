import easyocr
import cv2
import re

reader = easyocr.Reader(['en'], gpu=False)

def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Upscale for better OCR (slightly reduced from 2.5 → stable)
    gray = cv2.resize(
        gray, None,
        fx=2.2, fy=2.2,
        interpolation=cv2.INTER_CUBIC
    )

    # Noise reduction (better than only Gaussian)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # Adaptive threshold (best for number plates)
    gray = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    return gray


def read_plate(img):
    if img is None or img.size < 4000:
        return None

    proc = preprocess(img)

    results = reader.readtext(
        proc,
        allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
        paragraph=False
    )

    best_text = None
    best_conf = 0

    for r in results:
        text, conf = r[1], r[2]
        if conf > best_conf:
            best_text = text
            best_conf = conf

    if not best_text or best_conf < 0.40:
        return None

    # Clean text
    text = re.sub(r'[^A-Z0-9]', '', best_text.upper())

    # Indian plate length filter (safe range)
    return text if 7 <= len(text) <= 11 else None
