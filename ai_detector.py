import cv2
import torch
from ultralytics import YOLO
from backend.plate_ocr import read_plate

torch.set_grad_enabled(False)

# ---------------- MODELS ----------------
vehicle_model = YOLO("models/yolov8s.pt")   # vehicle + person
helmet_model  = YOLO("models/helmet.pt")
plate_model   = YOLO("models/plate.pt")

# ---------------- CONFIG ----------------
CONF_VEHICLE = 0.30
CONF_HELMET  = 0.35
CONF_PLATE   = 0.35
IMG_SIZE = 640

# ---------------- PLATE STABILITY ----------------
last_plate_text = None
plate_hits = 0
PLATE_CONFIRM = 3


def analyze_event(frame):
    global last_plate_text, plate_hits

    overlay = frame.copy()

    result = {
        "vehicle_type": None,
        "helmet": "NA",
        "plate": None,
        "decision": "WAIT"
    }

    # ---------------- VEHICLE + PERSON ----------------
    det = vehicle_model(
        frame,
        conf=CONF_VEHICLE,
        imgsz=IMG_SIZE,
        verbose=False
    )[0]

    vehicles = []
    persons = []

    for box, cls in zip(det.boxes.xyxy, det.boxes.cls):
        label = vehicle_model.names[int(cls)]
        x1, y1, x2, y2 = map(int, box)
        area = (x2 - x1) * (y2 - y1)

        if label in ["car", "motorcycle", "bus", "truck"]:
            vehicles.append((area, label, x1, y1, x2, y2))

        elif label == "person":
            persons.append((area, x1, y1, x2, y2))

    if not vehicles:
        return result, overlay

    vehicles.sort(reverse=True)
    _, vlabel, vx1, vy1, vx2, vy2 = vehicles[0]
    result["vehicle_type"] = vlabel.upper()

    # Vehicle box
    cv2.rectangle(overlay, (vx1, vy1), (vx2, vy2), (0, 255, 0), 2)
    cv2.putText(
        overlay,
        vlabel.upper(),
        (vx1, vy1 - 8),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    # ---------------- PERSON ----------------
    person_box = None
    if persons:
        persons.sort(reverse=True)
        _, px1, py1, px2, py2 = persons[0]
        person_box = (px1, py1, px2, py2)

        cv2.rectangle(overlay, (px1, py1), (px2, py2), (255, 255, 0), 2)
        cv2.putText(
            overlay,
            "PERSON",
            (px1, py1 - 6),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 0),
            2
        )

    # ---------------- HELMET (BIKE ONLY) ----------------
    if vlabel == "motorcycle":
        if person_box:
            px1, py1, px2, py2 = person_box
            helmet_zone = frame[
                py1:int(py1 + 0.4 * (py2 - py1)),
                px1:px2
            ]
        else:
            bh = vy2 - vy1
            helmet_zone = frame[
                vy1:int(vy1 + 0.35 * bh),
                vx1:vx2
            ]

        h = helmet_model(
            helmet_zone,
            conf=CONF_HELMET,
            imgsz=640,
            verbose=False
        )[0]

        result["helmet"] = "HELMET" if len(h.boxes) > 0 else "NO_HELMET"
        h_color = (0, 255, 255) if result["helmet"] == "HELMET" else (0, 0, 255)

        cv2.putText(
            overlay,
            result["helmet"],
            (vx1, vy1 + 22),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            h_color,
            2
        )

    # ---------------- NUMBER PLATE + OCR ----------------
    if vlabel == "car" or result["helmet"] == "HELMET":
        vh = vy2 - vy1
        plate_zone = frame[
            int(vy1 + 0.55 * vh):vy2,
            vx1:vx2
        ]

        p = plate_model(
            plate_zone,
            conf=CONF_PLATE,
            imgsz=IMG_SIZE,
            verbose=False
        )[0]

        if len(p.boxes) > 0:
            px1, py1, px2, py2 = map(int, p.boxes.xyxy[0])

            ax1 = vx1 + px1
            ay1 = int(vy1 + 0.55 * vh) + py1
            ax2 = vx1 + px2
            ay2 = int(vy1 + 0.55 * vh) + py2

            cv2.rectangle(overlay, (ax1, ay1), (ax2, ay2), (255, 0, 0), 2)

            crop = frame[ay1:ay2, ax1:ax2]
            if crop.size > 4000:
                text = read_plate(crop)

                if text:
                    if text == last_plate_text:
                        plate_hits += 1
                    else:
                        last_plate_text = text
                        plate_hits = 1

                    if plate_hits >= PLATE_CONFIRM:
                        result["plate"] = text

                        cv2.putText(
                            overlay,
                            text,
                            (ax1, ay1 - 6),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.65,
                            (255, 0, 0),
                            2
                        )

    # ---------------- FINAL DECISION ----------------
    if vlabel == "car":
        result["decision"] = "ALLOW" if result["plate"] else "WAIT"
    else:
        result["decision"] = "ALLOW" if result["helmet"] == "HELMET" else "BLOCK"

    return result, overlay
