import cv2
import time
import threading
from flask import Flask, Response, jsonify
from flask_cors import CORS
from queue import Queue

from backend.ai_detector import analyze_event
from backend.db_helper import log_gate_event

# ---------------- APP ----------------
app = Flask(__name__)
CORS(app)

RTSP_URL = "rtsp://admin:Imagic%40206@10.10.4.60:554/cam/realmonitor?channel=1&subtype=0"
CAMERA_NAME = "ENTRY_CAM"

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
if not cap.isOpened():
    print("❌ CAMERA NOT CONNECTED")
    exit()

print("✅ CAMERA CONNECTED")

latest_frame = None
latest_overlay = None
latest_result = {
    "vehicle_type": None,
    "plate": None,
    "helmet": "NA",
    "decision": "WAIT"
}

AI_INTERVAL = 1.8
last_ai_time = 0

db_queue = Queue(maxsize=50)

# ---------------- CAMERA THREAD ----------------
def camera_reader():
    global latest_frame
    while True:
        ret, frame = cap.read()
        if not ret:
            cap.release()
            time.sleep(1)
            cap.open(RTSP_URL)
            continue

        latest_frame = cv2.resize(frame, (854, 480))

# ---------------- AI THREAD ----------------
def ai_worker():
    global latest_overlay, latest_result, last_ai_time

    while True:
        if latest_frame is None:
            time.sleep(0.1)
            continue

        now = time.time()
        if now - last_ai_time < AI_INTERVAL:
            time.sleep(0.05)
            continue

        # Run AI on smaller frame for performance
        small = cv2.resize(latest_frame, (640, 360))
        result, overlay_small = analyze_event(small)

        # Scale overlay back to stream size
        latest_overlay = cv2.resize(overlay_small, (854, 480))
        latest_result = result
        last_ai_time = now

        # Push DB write asynchronously
        if result["decision"] != "WAIT" and result.get("plate"):
            try:
                db_queue.put_nowait(result)
            except:
                pass

# ---------------- DB THREAD ----------------
def db_worker():
    while True:
        data = db_queue.get()
        try:
            log_gate_event(
                CAMERA_NAME,
                data["vehicle_type"],
                data["plate"],
                data["helmet"],
                data["decision"]
            )
        except:
            pass
        db_queue.task_done()

# ---------------- STREAM ----------------
def generate_frames():
    while True:
        if latest_frame is None:
            time.sleep(0.05)
            continue

        frame = (
            latest_overlay.copy()
            if latest_overlay is not None
            else latest_frame.copy()
        )

        # ---------- GATE STATUS ----------
        decision = latest_result.get("decision", "WAIT")
        d_color = (0, 255, 0) if decision == "ALLOW" else (0, 0, 255)
        cv2.putText(
            frame,
            f"GATE: {decision}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            d_color,
            3
        )

        # ---------- LIVE NUMBER PLATE ----------
        plate = latest_result.get("plate")
        if plate:
            cv2.putText(
                frame,
                f"PLATE: {plate}",
                (20, 85),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 0, 0),
                2
            )

        # ---------- STREAM ----------
        ok, buffer = cv2.imencode(
            ".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 70]
        )
        if not ok:
            continue

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            buffer.tobytes() +
            b"\r\n"
        )

# ---------------- ROUTES ----------------
@app.route("/video")
def video():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/status")
def status():
    return jsonify(latest_result)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    print("🚀 Backend running at http://127.0.0.1:5000/video")
    threading.Thread(target=camera_reader, daemon=True).start()
    threading.Thread(target=ai_worker, daemon=True).start()
    threading.Thread(target=db_worker, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, threaded=True)
