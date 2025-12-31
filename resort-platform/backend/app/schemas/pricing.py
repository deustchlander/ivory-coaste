from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class PricingBase(BaseModel):
    room_id: int
    start_date: date
    end_date: date
    price: Decimal
    name: Optional[str] = None


class PricingCreate(PricingBase):
    pass


class PricingUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    price: Optional[Decimal] = None
    name: Optional[str] = None


class PricingOut(PricingBase):
    id: int

    class Config:
        from_attributes = True
