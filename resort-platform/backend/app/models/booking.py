from datetime import date, datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Booking(Base):
    """
    Represents a room booking made by a guest.
    """

    __tablename__ = "bookings"

    # -------------------------------------------------
    # Primary Key
    # -------------------------------------------------
    id = Column(Integer, primary_key=True, index=True)

    # -------------------------------------------------
    # Relationships
    # -------------------------------------------------
    room_id = Column(
        Integer,
        ForeignKey("rooms.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # -------------------------------------------------
    # Guest snapshot data
    # -------------------------------------------------
    guest_name = Column(String(255), nullable=False)
    guest_email = Column(String(255), nullable=False, index=True)
    guest_phone = Column(String(50), nullable=False)

    # -------------------------------------------------
    # Stay details
    # -------------------------------------------------
    check_in = Column(Date, nullable=False, index=True)
    check_out = Column(Date, nullable=False, index=True)
    adults = Column(Integer, nullable=False, default=1)
    children = Column(Integer, nullable=False, default=0)

    # -------------------------------------------------
    # Financials
    # -------------------------------------------------
    total_amount = Column(Numeric(10, 2), nullable=False)

    # -------------------------------------------------
    # Status & metadata
    # -------------------------------------------------
    status = Column(
        String(50),
        nullable=False,
        default="CONFIRMED",  # CONFIRMED | CANCELLED | COMPLETED
        index=True,
    )

    special_requests = Column(Text, nullable=True)

    # -------------------------------------------------
    # Timestamps
    # -------------------------------------------------
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # -------------------------------------------------
    # ORM Relationships
    # -------------------------------------------------
    room = relationship(
        "Room",
        back_populates="bookings",
        lazy="joined",
    )

    payments = relationship(
        "Payment",
        back_populates="booking",
        cascade="all, delete-orphan",
    )

    review = relationship(
        "Review",
        back_populates="booking",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Booking id={self.id} "
            f"room_id={self.room_id} "
            f"check_in={self.check_in} "
            f"check_out={self.check_out} "
            f"status={self.status}>"
        )
