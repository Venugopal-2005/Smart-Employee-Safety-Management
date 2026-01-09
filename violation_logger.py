import cv2
from datetime import datetime
import os

os.makedirs("violations", exist_ok=True)

def save_violation(frame, plate):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = plate if plate else "UNKNOWN"
    path = f"violations/{name}_{ts}.jpg"
    cv2.imwrite(path, frame)
    return path
