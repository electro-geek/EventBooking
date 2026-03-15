from app.db.models import User, Event

async def send_booking_confirmation(user_email: str, event_title: str):
    # Simulate sending email
    print(f"[BACKGROUND TASK] Sending booking confirmation email to {user_email} for event '{event_title}'")

async def notify_event_update(user_emails: list[str], event_title: str):
    # Simulate sending notifications
    for email in user_emails:
        print(f"[BACKGROUND TASK] Notifying {email} about update to event '{event_title}'")
