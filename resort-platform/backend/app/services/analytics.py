from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.booking import Booking
from app.models.payment import Payment


def get_booking_count(db: Session) -> int:
    """
    Return total number of bookings.
    """
    return db.query(func.count(Booking.id)).scalar() or 0


def get_total_revenue(db: Session):
    """
    Return total paid revenue.
    """
    return (
        db.query(func.coalesce(func.sum(Payment.amount), 0))
        .filter(Payment.status == "PAID")
        .scalar()
    )
