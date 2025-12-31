from typing import Optional

from pydantic import BaseModel, EmailStr


class GuestBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None


class GuestCreate(GuestBase):
    password: Optional[str] = None


class GuestUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None


class GuestOut(GuestBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True
