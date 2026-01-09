import cv2

RTSP_URL = "rtsp://admin:Imagic%40206@10.10.4.60:554/cam/realmonitor?channel=1&subtype=1"


cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("❌ Camera NOT opened")
    exit()

print("✅ Camera opened")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Frame not received")
        break

    cv2.imshow("CP PLUS LIVE", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
