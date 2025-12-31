from typing import Optional

from app.core.logging import setup_logging

setup_logging()


def send_booking_confirmation_sms(
    phone_number: str,
    booking_id: int,
    guest_name: Optional[str] = None,
) -> None:
    """
    Send booking confirmation SMS.
    Replace with real SMS gateway (Twilio, MSG91, etc.).
    """
    message = (
        f"Dear {guest_name or 'Guest'}, "
        f"your booking (ID: {booking_id}) is confirmed. "
        f"Thank you for choosing our resort."
    )

    # Placeholder – integrate SMS gateway here
    print(f"[SMS] To: {phone_number} | Message: {message}")


def send_payment_confirmation_sms(
    phone_number: str,
    amount: str,
) -> None:
    """
    Send payment confirmation SMS.
    """
    message = f"Payment of {amount} received successfully. Thank you."

    print(f"[SMS] To: {phone_number} | Message: {message}")
