from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class BookingBase(BaseModel):
    room_id: int
    guest_name: str
    guest_email: str
    guest_phone: str
    check_in: date
    check_out: date
    adults: int
    children: int
    total_amount: Decimal
    special_requests: Optional[str] = None


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    check_in: Optional[date] = None
    check_out: Optional[date] = None
    adults: Optional[int] = None
    children: Optional[int] = None
    total_amount: Optional[Decimal] = None
    status: Optional[str] = None
    special_requests: Optional[str] = None


class BookingOut(BookingBase):
    id: int
    status: str

    class Config:
        from_attributes = True
