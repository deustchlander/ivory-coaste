from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.booking import Booking


def cancel_expired_unpaid_bookings(
    db: Session,
    expiry_minutes: int = 60,
) -> int:
    """
    Cancel bookings that were never paid within the expiry window.
    Returns number of cancelled bookings.
    """
    cutoff_time = datetime.utcnow() - timedelta(minutes=expiry_minutes)

    bookings = (
        db.query(Booking)
        .filter(
            Booking.status == "CONFIRMED",
            Booking.created_at < cutoff_time,
        )
        .all()
    )

    cancelled_count = 0

    for booking in bookings:
        booking.status = "CANCELLED"
        cancelled_count += 1

    if cancelled_count > 0:
        db.commit()

    return cancelled_count
