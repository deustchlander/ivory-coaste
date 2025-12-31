from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class PaymentBase(BaseModel):
    booking_id: int
    amount: Decimal
    method: str
    reference_id: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    status: Optional[str] = None
    reference_id: Optional[str] = None


class PaymentOut(PaymentBase):
    id: int
    status: str
    paid_at: Optional[datetime] = None

    class Config:
        from_attributes = True
