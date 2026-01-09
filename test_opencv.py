import cv2, time
from ultralytics import YOLO
from backend.plate_ocr import read_plate

RTSP_URL = "rtsp://admin:Imagic%40206@10.10.4.60:554/cam/realmonitor?channel=1&subtype=1"
plate_model = YOLO("models/plate.pt")

TARGET_W, TARGET_H = 640, 360
PLATE_CONF = 0.30
OCR_EVERY_N = 15

def open_cam():
    cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return cap

cap = open_cam()
last_plate = None
ocr_id = 0
prev = time.time()

while True:
    for _ in range(5):
        cap.grab()

    ret, frame = cap.read()
    if not ret:
        cap.release()
        time.sleep(1)
        cap = open_cam()
        continue

    frame = cv2.resize(frame, (TARGET_W, TARGET_H))
    res = plate_model(frame, conf=PLATE_CONF, imgsz=960, verbose=False)[0]

    if len(res.boxes) > 0:
        x1,y1,x2,y2 = map(int, res.boxes.xyxy[0])
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,255), 2)
        crop = frame[y1:y2, x1:x2]
        ocr_id += 1
        if crop.size > 3000 and ocr_id % OCR_EVERY_N == 0:
            txt = read_plate(crop)
            if txt:
                last_plate = txt

    if last_plate:
        cv2.putText(frame, f"PLATE: {last_plate}", (20,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    fps = int(1 / max(time.time()-prev, 1e-6))
    prev = time.time()
    cv2.putText(frame, f"FPS: {fps}", (20,60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.imshow("PLATE TEST (NO LAG)", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
