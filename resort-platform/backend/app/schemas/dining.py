from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class DiningBase(BaseModel):
    name: str
    description: Optional[str] = None
    meal_type: str
    price: Optional[Decimal] = None
    is_vegetarian: bool = True
    is_available: bool = True
    display_order: int = 0


class DiningCreate(DiningBase):
    pass


class DiningUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    meal_type: Optional[str] = None
    price: Optional[Decimal] = None
    is_vegetarian: Optional[bool] = None
    is_available: Optional[bool] = None
    display_order: Optional[int] = None


class DiningOut(DiningBase):
    id: int

    class Config:
        from_attributes = True
