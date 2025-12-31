def send_booking_confirmation(
    email: str,
    booking_id: int,
) -> None:
    """
    Stub for sending booking confirmation email.
    Replace with real email provider integration.
    """
    # Example: SendGrid, SES, SMTP
    print(f"[EMAIL] Booking confirmation sent to {email} (Booking ID: {booking_id})")


def send_payment_confirmation(
    email: str,
    amount: str,
) -> None:
    """
    Stub for sending payment confirmation.
    """
    print(f"[EMAIL] Payment of {amount} confirmed for {email}")
