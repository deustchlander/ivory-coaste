from typing import Optional

from app.core.logging import setup_logging

# Initialize logging (safe if called multiple times)
setup_logging()


def send_booking_confirmation_email(
    to_email: str,
    booking_id: int,
    guest_name: Optional[str] = None,
) -> None:
    """
    Send booking confirmation email.
    Replace implementation with real email provider.
    """
    subject = "Your Resort Booking is Confirmed"
    message = (
        f"Hello {guest_name or 'Guest'},\n\n"
        f"Your booking (ID: {booking_id}) has been confirmed.\n"
        f"We look forward to hosting you.\n\n"
        f"Regards,\nResort Team"
    )

    # Placeholder – integrate SendGrid / SES / SMTP here
    print(f"[EMAIL] To: {to_email}\nSubject: {subject}\n\n{message}")


def send_payment_receipt_email(
    to_email: str,
    amount: str,
    booking_id: int,
) -> None:
    """
    Send payment receipt email.
    """
    subject = "Payment Received"
    message = (
        f"Hello,\n\n"
        f"We have received your payment of {amount} "
        f"for booking ID {booking_id}.\n\n"
        f"Thank you,\nResort Team"
    )

    print(f"[EMAIL] To: {to_email}\nSubject: {subject}\n\n{message}")
