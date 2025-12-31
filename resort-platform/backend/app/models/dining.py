from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Numeric,
    DateTime,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class DiningItem(Base):
    """
    Represents a dining menu item or meal plan.
    """

    __tablename__ = "dining_items"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    meal_type = Column(String(50), nullable=False)  # BREAKFAST | LUNCH | DINNER | PLAN

    price = Column(Numeric(10, 2), nullable=True)

    is_vegetarian = Column(Boolean, nullable=False, default=True)
    is_available = Column(Boolean, nullable=False, default=True)

    display_order = Column(Integer, nullable=False, default=0)

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    def __repr__(self) -> str:
        return f"<DiningItem id={self.id} name={self.name}>"
