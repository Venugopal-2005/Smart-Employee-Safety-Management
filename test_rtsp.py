import cv2

RTSP_URL = "rtsp://admin:Imagic%40206@10.10.4.60:554/cam/realmonitor?channel=1&subtype=0"

cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("❌ RTSP NOT OPENED")
    exit()

print("✅ RTSP CONNECTED")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Frame failed")
        break

    cv2.imshow("RTSP TEST", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
