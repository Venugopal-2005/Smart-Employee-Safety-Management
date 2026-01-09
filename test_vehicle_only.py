import cv2
import time

RTSP_URL = "rtsp://admin:Imagic%40206@10.10.4.60:554/cam/realmonitor?channel=1&subtype=0"

cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("❌ CAMERA NOT CONNECTED")
    exit()

print("✅ CAMERA CONNECTED")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Frame not received")
        time.sleep(1)
        continue

    cv2.imshow("CAMERA TEST", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
