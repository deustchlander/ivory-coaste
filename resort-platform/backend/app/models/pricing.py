from datetime import date

from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    Date,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class PricingRule(Base):
    """
    Represents a seasonal or date-based pricing rule.
    """

    __tablename__ = "pricing_rules"

    id = Column(Integer, primary_key=True, index=True)

    room_id = Column(
        Integer,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name = Column(String(255), nullable=True)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    price = Column(Numeric(10, 2), nullable=False)

    room = relationship(
        "Room",
        back_populates="pricing_rules",
    )

    def __repr__(self) -> str:
        return f"<PricingRule id={self.id} room_id={self.room_id} price={self.price}>"
