# notification_engine.py
import mysql.connector
from datetime import datetime, timedelta

IMPORTANT_EVENTS = {
    "Motion Detected",
    "Door Opened",
    "Window Opened",
    "System Disarmed"
}

def db_connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="hello",
        database="project"
    )


def fetch_invoice_notifications():
    conn = db_connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT Invoice_ID, Customer_ID, Invoice_Deadline
        FROM invoice
        WHERE Status != '1'
    """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    today = datetime.now().date()
    output = []

    for row in rows:
        deadline = row["Invoice_Deadline"]
        if isinstance(deadline, datetime):
            deadline = deadline.date()

        if deadline - today <= timedelta(days=7):
            output.append({
                "id": row["Invoice_ID"],
                "type": "invoice",
                "message": f"Invoice {row['Invoice_ID']} due {deadline}",
                "date": deadline,
                "is_read": False
            })

    return output


def fetch_event_notifications():
    conn = db_connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT Event_ID, Customer_ID, Event_Date, Event_Time, Event_type
        FROM event_log
        ORDER BY Event_Date DESC, Event_Time DESC
        LIMIT 50
    """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    output = []

    for row in rows:
        if row["Event_type"] in IMPORTANT_EVENTS:
            output.append({
                "id": row["Event_ID"],
                "type": "event",
                "message": f"{row['Event_type']} at {row['Event_Time']}",
                "date": row["Event_Date"],
                "is_read": False
            })

    return output


def fetch_payment_notifications():
    conn = db_connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT log_number, Customer_ID, Invoice_ID, Date_Paid, Days_left
        FROM paymentlog
    """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    output = []

    for row in rows:
        if (row["Days_left"] !=0) and  (row["Days_left"] <= 2):
            output.append({
                "id": row["log_number"],
                "type": "payment",
                "message": f"Customer {row['Customer_ID']} paid with only {row['Days_left']} days left",
                "date": row["Date_Paid"],
                "is_read": False
            })

    return output


def scan_for_notifications():
    invoices = fetch_invoice_notifications()
    events = fetch_event_notifications()
    payments = fetch_payment_notifications()

    return invoices + events + payments
