from typing import Optional

from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    booking_id: int
    guest_name: str
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    comment: Optional[str] = None
    is_approved: Optional[bool] = None


class ReviewOut(ReviewBase):
    id: int
    is_approved: bool

    class Config:
        from_attributes = True
