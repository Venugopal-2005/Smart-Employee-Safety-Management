from ultralytics import YOLO

vehicle_model = YOLO("models/yolov8n.pt")

def detect_vehicle(frame):
    results = vehicle_model(frame, conf=0.4, verbose=False)[0]
    for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
        label = vehicle_model.names[int(cls)]
        if label in ["motorcycle", "car"]:
            return label.upper(), box
    return None, None
