import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",          # ✅ your correct password
        database="smart_vehicle_db",
        autocommit=True
    )

def log_gate_event(camera, vehicle, plate, helmet, decision):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO gate_events
            (camera_name, vehicle_type, plate_number, helmet_status, decision)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (camera, vehicle, plate, helmet, decision)
        )
        cur.close()
        conn.close()
    except Exception as e:
        print("⚠️ DB write skipped:", e)
