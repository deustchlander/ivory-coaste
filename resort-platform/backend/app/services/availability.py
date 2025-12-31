from datetime import date
from sqlalchemy.orm import Session

from app.models.booking import Booking


def is_room_available(
    db: Session,
    room_id: int,
    check_in: date,
    check_out: date,
) -> bool:
    """
    Check whether a room is available for the given date range.
    """
    overlapping_booking = (
        db.query(Booking)
        .filter(
            Booking.room_id == room_id,
            Booking.status == "CONFIRMED",
            Booking.check_in < check_out,
            Booking.check_out > check_in,
        )
        .first()
    )

    return overlapping_booking is None
