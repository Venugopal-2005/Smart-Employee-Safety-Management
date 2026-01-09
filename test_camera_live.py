import cv2
from backend.ai_detector import analyze_frame

RTSP_URL = "rtsp://admin:Imagic%40206@10.10.4.60:554/cam/realmonitor?channel=1&subtype=1"

cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("❌ Camera not opened")
    exit()

print("✅ Camera connected")

cv2.namedWindow("LIVE DETECTION", cv2.WINDOW_NORMAL)
cv2.resizeWindow("LIVE DETECTION", 960, 540)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # ✅ CORRECT CALL (ONLY ONE ARGUMENT)
    result = analyze_frame(frame)

    cv2.imshow("LIVE DETECTION", result["frame"])

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
