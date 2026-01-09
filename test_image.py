import cv2
from backend.ai_detector import analyze_frame_full

IMAGE_PATH = "backend/test_images/detection/car.jpg"  # change if needed

img = cv2.imread(IMAGE_PATH)
if img is None:
    print("❌ Image not found:", IMAGE_PATH)
    exit()

# Slight upscale for accuracy
img = cv2.resize(img, None, fx=1.3, fy=1.3, interpolation=cv2.INTER_CUBIC)

frame, result = analyze_frame_full(img)

print("\n===== IMAGE TEST RESULT =====")
print("Vehicle Type :", result["vehicle_type"])
print("Helmet Status:", result["helmet_status"])
print("Plate Number :", result["plate_number"])
print("Decision     :", result["decision"])

cv2.namedWindow("IMAGE DETECTION", cv2.WINDOW_NORMAL)
cv2.resizeWindow("IMAGE DETECTION", 1000, 650)
cv2.imshow("IMAGE DETECTION", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
