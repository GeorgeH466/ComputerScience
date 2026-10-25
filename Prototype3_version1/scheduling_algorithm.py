import mysql.connector
from datetime import datetime


def db_connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="hello",
        database="project"
    )


def get_all_events():
    conn = db_connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT Event_ID, Customer_ID, Event_Date, Event_Time, Event_type
        FROM event_log
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    for row in rows:
        if isinstance(row["Event_Date"], datetime):
            row["Event_Date"] = row["Event_Date"].date()

        if isinstance(row["Event_Time"], datetime):
            row["Event_Time"] = row["Event_Time"].time()

    return rows


def add_event(new_event):
    existing_events = get_all_events()

    for event in existing_events:
        if (
            event["Event_Date"] == new_event["date"]
            and event["Event_Time"] == new_event["time"]
        ):
            return {
                "status": "clash",
                "clashing_event": event
            }

    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO event_log
        (Customer_ID, Event_Date, Event_Time, Event_type)
        VALUES (%s, %s, %s, %s)
    """, (
        new_event["customer"],
        new_event["date"],
        new_event["time"],
        new_event["type"]
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "status": "saved"
    }