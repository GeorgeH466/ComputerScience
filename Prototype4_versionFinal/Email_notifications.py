"""Email urgent scheduled-event notifications using configured SMTP settings."""

import os
import smtplib
from datetime import datetime
from email.message import EmailMessage

from database_connection import create_connection


def get_urgent_events():
    """Fetch important scheduled events and their customer email addresses."""
    connection = create_connection()
    if connection is None:
        raise RuntimeError("Could not connect to the project database.")

    cursor = connection.cursor(dictionary=True)
    try:
        # Select important event records and resolve each recipient from contacts.
        cursor.execute(
            "SELECT e.Event_ID AS id, e.Customer_ID AS customer_id, "
            "e.Event_type AS type, e.Event_Date AS date, e.Event_Time AS time, "
            "c.customer_name AS customer_name, ct.Email AS recipient_email "
            "FROM event_log e "
            "JOIN customer c ON c.Customer_ID = e.Customer_ID "
            "JOIN customer_contact ct ON ct.Customer_ID = e.Customer_ID "
            "WHERE e.Event_type IN (%s, %s, %s, %s) "
            "AND ct.Email IS NOT NULL AND ct.Email <> '' "
            "ORDER BY e.Event_Date DESC, e.Event_Time DESC",
            ("Motion Detected", "Door Opened", "Window Opened", "System Disarmed"),
        )
        return cursor.fetchall()
    finally:
        # Release database resources regardless of query outcome.
        cursor.close()
        connection.close()


def _smtp_settings():
    """Read SMTP connection settings from environment variables."""
    # Never embed account passwords in source; deployment supplies these values.
    host = os.getenv("SMTP_HOST", "")
    username = os.getenv("SMTP_USERNAME", "")
    password = os.getenv("SMTP_PASSWORD", "")
    sender = os.getenv("SMTP_FROM", username)

    # Host and sender are needed to create a useful, correctly addressed message.
    if not host or not sender:
        raise RuntimeError(
            "Set SMTP_HOST and SMTP_FROM (or SMTP_USERNAME) before sending email."
        )

    # Convert the configured port safely and provide standard SMTP defaults.
    try:
        port = int(os.getenv("SMTP_PORT", "587"))
    except ValueError as error:
        raise RuntimeError("SMTP_PORT must be a valid port number.") from error
    return host, port, username, password, sender


def check_email_notifications(email_enabled=True):
    """Send one notification per urgent event; return counts and any errors."""
    # Honor the feature toggle before making a database or network connection.
    if not email_enabled:
        return {"sent": 0, "failed": 0, "skipped": True}

    events = get_urgent_events()
    if not events:
        return {"sent": 0, "failed": 0, "skipped": False}

    # Validate required configuration once, before attempting any event emails.
    host, port, username, password, sender = _smtp_settings()
    sent = 0
    errors = []

    # Send each event with a fresh SMTP session so failures are isolated.
    for event in events:
        email = create_email_template(event, sender=sender)
        try:
            with smtplib.SMTP(host, port, timeout=20) as server:
                # Upgrade to TLS when the server supports the standard port.
                if port == 587:
                    server.starttls()
                # Authenticate only when credentials were explicitly configured.
                if username:
                    server.login(username, password)
                server.send_message(email)

            # Record success for this run and keep a timestamped local log.
            log_email_sent(event)
            sent += 1
        except (smtplib.SMTPException, OSError) as error:
            # Preserve the failure detail for the caller and continue other events.
            log_email_error(event, error)
            errors.append({"event_id": event.get("id"), "error": str(error)})

    return {"sent": sent, "failed": len(errors), "errors": errors, "skipped": False}


def create_email_template(event, sender=None):
    """Create an email containing the customer-facing event details."""
    # Resolve the sender from configuration when a caller did not supply it.
    if sender is None:
        sender = _smtp_settings()[4]

    # Build a standards-compliant email with a plain-text body.
    email = EmailMessage()
    email["Subject"] = f"URGENT EVENT: {event.get('type', 'Event')}"
    email["From"] = sender
    email["To"] = event["recipient_email"]
    email.set_content(
        "Urgent event notification\n\n"
        f"Event: {event.get('type', 'Unknown')}\n"
        f"Customer: {event.get('customer_name', 'Unknown')}\n"
        f"Date: {event.get('date', '')}\n"
        f"Time: {event.get('time', '')}\n\n"
        "Please review this event as soon as possible.\n"
    )
    return email


def log_email_sent(event):
    """Record a successful email send in the application's console log."""
    print(
        f"Email sent for event {event.get('id', event.get('type', 'unknown'))} "
        f"at {datetime.now().isoformat(timespec='seconds')}"
    )


def log_email_error(event, error):
    """Record a failed email send in the application's console log."""
    print(
        f"Failed to send email for event "
        f"{event.get('id', event.get('type', 'unknown'))}: {error}"
    )
