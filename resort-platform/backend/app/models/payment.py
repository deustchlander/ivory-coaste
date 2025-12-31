from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Payment(Base):
    """
    Represents a payment made towards a booking.
    """

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    amount = Column(Numeric(10, 2), nullable=False)

    method = Column(String(50), nullable=False)
    status = Column(
        String(50),
        nullable=False,
        default="PENDING",  # PENDING | PAID | FAILED
    )

    reference_id = Column(String(255), nullable=True)
    paid_at = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    booking = relationship(
        "Booking",
        back_populates="payments",
    )

    def __repr__(self) -> str:
        return f"<Payment id={self.id} booking_id={self.booking_id} amount={self.amount}>"
