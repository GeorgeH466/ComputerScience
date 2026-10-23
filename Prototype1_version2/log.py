
from datetime import date, datetime
from database_connection import create_connection


def get_actual_date():
    return date.today()#collects and returns the date of the event

def get_actual_time():
    return datetime.now().strftime("%H:%M:%S")#controls the format of the time string


def log_event(event_description):
    current_date = get_actual_date()
    current_time = get_actual_time()

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO log_table (event_description, event_date, event_time)
        VALUES (%s, %s, %s)
    """, (event_description, current_date, current_time))

    connection.commit()
    cursor.close()
    connection.close()
