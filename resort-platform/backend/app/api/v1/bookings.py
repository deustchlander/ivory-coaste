from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.booking import Booking
from app.models.room import Room
from app.models.guest import Guest
from app.schemas.booking import (
    BookingCreate,
    BookingOut,
    BookingUpdate,
)
from app.api.v1.auth import get_current_user

router = APIRouter()


# -------------------------------------------------
# Helper functions
# -------------------------------------------------

def check_room_availability(
    db: Session,
    room_id: int,
    check_in: date,
    check_out: date,
) -> bool:
    """
    Returns True if the room is available for the given date range.
    """
    overlapping = (
        db.query(Booking)
        .filter(
            Booking.room_id == room_id,
            Booking.check_in < check_out,
            Booking.check_out > check_in,
            Booking.status == "CONFIRMED",
        )
        .first()
    )
    return overlapping is None


# -------------------------------------------------
# Public Endpoints
# -------------------------------------------------

@router.post(
    "/",
    response_model=BookingOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a booking",
)
def create_booking(
    payload: BookingCreate,
    db: Session = Depends(get_db),
):
    room = db.query(Room).filter(Room.id == payload.room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    if payload.check_in >= payload.check_out:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date range",
        )

    if not check_room_availability(
        db,
        payload.room_id,
        payload.check_in,
        payload.check_out,
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Room not available for selected dates",
        )

    booking = Booking(
        room_id=payload.room_id,
        guest_name=payload.guest_name,
        guest_email=payload.guest_email,
        guest_phone=payload.guest_phone,
        check_in=payload.check_in,
        check_out=payload.check_out,
        adults=payload.adults,
        children=payload.children,
        total_amount=payload.total_amount,
        status="CONFIRMED",
        special_requests=payload.special_requests,
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


# -------------------------------------------------
# Admin Endpoints
# -------------------------------------------------

@router.get(
    "/",
    response_model=List[BookingOut],
    summary="List all bookings (admin)",
)
def list_bookings(
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    return (
        db.query(Booking)
        .order_by(Booking.check_in.desc())
        .all()
    )


@router.get(
    "/{booking_id}",
    response_model=BookingOut,
    summary="Get booking by ID (admin)",
)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )
    return booking


@router.put(
    "/{booking_id}",
    response_model=BookingOut,
    summary="Update booking (admin)",
)
def update_booking(
    booking_id: int,
    payload: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(booking, field, value)

    db.commit()
    db.refresh(booking)

    return booking


@router.delete(
    "/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel booking (admin)",
)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    booking.status = "CANCELLED"
    db.commit()

    return None
