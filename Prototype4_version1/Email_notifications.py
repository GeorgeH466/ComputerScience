```python
import smtplib
from email.message import EmailMessage
from datetime import datetime


def check_email_notifications(email_enabled):

    # Get urgent events from the database
    events = get_urgent_events()

    # Send an email for each urgent event
    for event in events:

        # Create the email
        email = create_email_template(event)

        try:
            # Connect to the email server
            with smtplib.SMTP("smtp.example.com", 587) as server:

                # Secure the connection
                server.starttls()

                # Log in to the email account
                server.login(
                    "system@example.com",
                    "EMAIL_PASSWORD"
                )

                # Send the email
                server.send_message(email)

            # Log that the email was successfully sent
            log_email_sent(event)

        except smtplib.SMTPException as error:
            # Log an error if the email could not be sent
            log_email_error(event, error)


def create_email_template(event):
    """Create an email containing information about the urgent event."""

    email = EmailMessage()

    email["Subject"] = "URGENT EVENT: " + event["type"]
    email["From"] = "system@example.com"
    email["To"] = event["recipient_email"]

    email.set_content(
        f"""
Urgent event notification

Event: {event["type"]}
Customer: {event["customer_name"]}
Date: {event["date"]}
Time: {event["time"]}

Details:
{event["description"]}

Please review this event as soon as possible.
"""
    )

    return email


def log_email_sent(event):
    """Record that an email was successfully sent."""

    print(
        f"Email sent successfully for event "
        f"{event['type']} at {datetime.now()}"
    )


def log_email_error(event, error):
    """Record that an email failed to send."""

    print(
        f"Failed to send email for event "
        f"{event['type']}: {error}"
    )
```