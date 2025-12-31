from typing import Any, Optional
from decimal import Decimal

from pydantic import BaseModel


class RoomBase(BaseModel):
    name: str
    description: Optional[str] = None
    base_price: Decimal
    max_adults: int
    max_children: int
    amenities: Optional[Any] = None
    is_active: bool = True
    display_order: int = 0


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    base_price: Optional[Decimal] = None
    max_adults: Optional[int] = None
    max_children: Optional[int] = None
    amenities: Optional[Any] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


class RoomOut(RoomBase):
    id: int

    class Config:
        from_attributes = True
