from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Numeric,
    DateTime,
    JSON,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Room(Base):
    """
    Represents a room or villa in the resort.
    """

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    base_price = Column(Numeric(10, 2), nullable=False)

    max_adults = Column(Integer, nullable=False, default=2)
    max_children = Column(Integer, nullable=False, default=0)

    amenities = Column(JSON, nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)
    display_order = Column(Integer, nullable=False, default=0)

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

    bookings = relationship(
        "Booking",
        back_populates="room",
    )

    pricing_rules = relationship(
        "PricingRule",
        back_populates="room",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Room id={self.id} name={self.name}>"
