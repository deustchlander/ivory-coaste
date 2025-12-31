from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.guest import Guest
from app.schemas.guest import (
    GuestCreate,
    GuestOut,
    GuestUpdate,
)
from app.api.v1.auth import get_current_user

router = APIRouter()


# -------------------------------------------------
# Admin Endpoints
# -------------------------------------------------

@router.get(
    "/",
    response_model=List[GuestOut],
    summary="List all guests (admin)",
)
def list_guests(
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    return (
        db.query(Guest)
        .order_by(Guest.created_at.desc())
        .all()
    )


@router.get(
    "/{guest_id}",
    response_model=GuestOut,
    summary="Get guest by ID (admin)",
)
def get_guest(
    guest_id: int,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guest not found",
        )
    return guest


@router.post(
    "/",
    response_model=GuestOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create guest record (admin)",
)
def create_guest(
    payload: GuestCreate,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    existing = db.query(Guest).filter(Guest.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Guest with this email already exists",
        )

    guest = Guest(
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        is_admin=False,
    )

    db.add(guest)
    db.commit()
    db.refresh(guest)

    return guest


@router.put(
    "/{guest_id}",
    response_model=GuestOut,
    summary="Update guest record (admin)",
)
def update_guest(
    guest_id: int,
    payload: GuestUpdate,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guest not found",
        )

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(guest, field, value)

    db.commit()
    db.refresh(guest)

    return guest


@router.delete(
    "/{guest_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete guest record (admin)",
)
def delete_guest(
    guest_id: int,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guest not found",
        )

    db.delete(guest)
    db.commit()

    return None
