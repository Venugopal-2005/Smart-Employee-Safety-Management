import cv2
import time

RTSP_URL = "rtsp://admin:Imagic%40206@10.10.4.60:554/cam/realmonitor?channel=1&subtype=1"

# ================= SETTINGS (SPEED FIRST) =================
TARGET_W, TARGET_H = 480, 270  # VERY FAST
SKIP_FRAMES = 3                # Drop frames to avoid lag

def open_camera():
    cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return cap

cap = open_camera()
frame_id = 0
prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("⚠️ Frame lost, reconnecting...")
        cap.release()
        time.sleep(1)
        cap = open_camera()
        continue

    frame_id += 1
    if frame_id % SKIP_FRAMES != 0:
        continue  # DROP FRAME (IMPORTANT)

    frame = cv2.resize(frame, (TARGET_W, TARGET_H))

    # ===== FPS DISPLAY =====
    now = time.time()
    fps = 1 / (now - prev_time)
    prev_time = now

    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.imshow("RAW CAMERA TEST (FAST)", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
