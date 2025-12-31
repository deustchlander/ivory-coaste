from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Review(Base):
    """
    Represents a guest review linked to a booking.
    """

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    guest_name = Column(String(255), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)

    is_approved = Column(Boolean, nullable=False, default=False)

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    booking = relationship(
        "Booking",
        back_populates="review",
    )

    def __repr__(self) -> str:
        return f"<Review id={self.id} rating={self.rating} approved={self.is_approved}>"
