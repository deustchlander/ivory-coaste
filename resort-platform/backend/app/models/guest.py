from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Guest(Base):
    """
    Represents a guest or admin user.
    """

    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(50), nullable=True)

    hashed_password = Column(String(255), nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    def __repr__(self) -> str:
        return f"<Guest id={self.id} email={self.email} admin={self.is_admin}>"
