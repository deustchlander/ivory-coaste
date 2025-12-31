from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.payment import Payment


def record_payment(
    db: Session,
    booking_id: int,
    amount: Decimal,
    method: str,
    reference_id: str | None = None,
) -> Payment:
    """
    Record a payment against a booking.
    """
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise ValueError("Booking not found")

    payment = Payment(
        booking_id=booking_id,
        amount=amount,
        method=method,
        status="PENDING",
        reference_id=reference_id,
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


def mark_payment_paid(
    db: Session,
    payment: Payment,
) -> Payment:
    """
    Mark a payment as PAID.
    """
    payment.status = "PAID"
    db.commit()
    db.refresh(payment)
    return payment
