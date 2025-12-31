from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.room import Room
from app.schemas.room import (
    RoomCreate,
    RoomOut,
    RoomUpdate,
)
from app.models.guest import Guest
from app.api.v1.auth import get_current_user

router = APIRouter()


# -------------------------------------------------
# Public Endpoints
# -------------------------------------------------

@router.get(
    "/",
    response_model=List[RoomOut],
    summary="List all active rooms",
)
def list_rooms(
    db: Session = Depends(get_db),
):
    """
    Public endpoint to list rooms available for booking.
    Only rooms marked as active are returned.
    """
    return (
        db.query(Room)
        .filter(Room.is_active.is_(True))
        .order_by(Room.display_order.asc())
        .all()
    )


@router.get(
    "/{room_id}",
    response_model=RoomOut,
    summary="Get room details",
)
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room or not room.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )
    return room


# -------------------------------------------------
# Admin Endpoints
# -------------------------------------------------

@router.post(
    "/",
    response_model=RoomOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create room (admin)",
)
def create_room(
    payload: RoomCreate,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    room = Room(
        name=payload.name,
        description=payload.description,
        base_price=payload.base_price,
        max_adults=payload.max_adults,
        max_children=payload.max_children,
        amenities=payload.amenities,
        is_active=payload.is_active,
        display_order=payload.display_order,
    )

    db.add(room)
    db.commit()
    db.refresh(room)

    return room


@router.put(
    "/{room_id}",
    response_model=RoomOut,
    summary="Update room (admin)",
)
def update_room(
    room_id: int,
    payload: RoomUpdate,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(room, field, value)

    db.commit()
    db.refresh(room)

    return room


@router.delete(
    "/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete room (admin)",
)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    db.delete(room)
    db.commit()

    return None
