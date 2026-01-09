# camera_config.py
# Central place for all camera-related configuration

# =========================
# CAMERA CONNECTIONS
# =========================

CAMERAS = {
    "ENTRY_CAM": {
        "type": "RTSP",
        "url": "rtsp://admin:mspl%40123@192.168.1.100:554/onvif/profile1/media.smp",
        "location": "Gate Entry",
        "direction": "ENTRY",
        "auto_zoom": True
    },

    # Example for second camera (optional)
    # "OUTSIDE_CAM": {
    #     "type": "RTSP",
    #     "url": "rtsp://admin:password@192.168.1.196:554/onvif/profile1/media.smp",
    #     "location": "Gate Outside",
    #     "direction": "EXIT",
    #     "auto_zoom": True
    # }
}

# =========================
# VIDEO PROCESSING SETTINGS
# =========================

FRAME_SKIP = 2          # process every Nth frame (performance)
CONF_THRESHOLD = 0.4    # YOLO confidence
PLATE_MIN_AREA = 5000   # ignore tiny plate regions

# =========================
# DAY / NIGHT DETECTION
# =========================

NIGHT_MODE = {
    "enable": True,
    "brightness_threshold": 60,   # below this = night
    "use_ir": True
}

# =========================
# DECISION RULES
# =========================

RULES = {
    "MOTORCYCLE": {
        "helmet_required": True,
        "no_plate_action": "BLOCK"
    },
    "CAR": {
        "helmet_required": False,
        "no_plate_action": "BLOCK"
    }
}

# =========================
# GATE CONTROL
# =========================

GATE = {
    "enable": True,
    "open_duration_sec": 5,
    "block_on_unknown_helmet": True
}

# =========================
# VIOLATION LOGGING
# =========================

VIOLATION = {
    "save_images": True,
    "save_path": "violations/",
    "image_quality": 90
}

# =========================
# ALERT SETTINGS
# =========================

ALERTS = {
    "enable": True,
    "whatsapp": True,
    "email": True
}
