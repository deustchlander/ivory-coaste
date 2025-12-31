from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.pricing import PricingRule
from app.models.room import Room
from app.schemas.pricing import (
    PricingCreate,
    PricingOut,
    PricingUpdate,
)
from app.models.guest import Guest
from app.api.v1.auth import get_current_user

router = APIRouter()


# -------------------------------------------------
# Public Endpoints
# -------------------------------------------------

@router.get(
    "/room/{room_id}",
    response_model=List[PricingOut],
    summary="Get pricing rules for a room",
)
def get_room_pricing(
    room_id: int,
    db: Session = Depends(get_db),
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    return (
        db.query(PricingRule)
        .filter(PricingRule.room_id == room_id)
        .order_by(PricingRule.start_date.asc())
        .all()
    )


@router.get(
    "/room/{room_id}/price",
    summary="Calculate room price for date range",
)
def calculate_price(
    room_id: int,
    check_in: date,
    check_out: date,
    db: Session = Depends(get_db),
):
    if check_in >= check_out:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date range",
        )

    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    rules = (
        db.query(PricingRule)
        .filter(PricingRule.room_id == room_id)
        .all()
    )

    total_price = 0
    current_date = check_in

    while current_date < check_out:
        daily_price = room.base_price

        for rule in rules:
            if rule.start_date <= current_date <= rule.end_date:
                daily_price = rule.price
                break

        total_price += daily_price
        current_date = current_date.fromordinal(current_date.toordinal() + 1)

    return {
        "room_id": room_id,
        "check_in": check_in,
        "check_out": check_out,
        "total_price": total_price,
        "currency": "INR",
    }


# -------------------------------------------------
# Admin Endpoints
# -------------------------------------------------

@router.post(
    "/",
    response_model=PricingOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create pricing rule (admin)",
)
def create_pricing_rule(
    payload: PricingCreate,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    room = db.query(Room).filter(Room.id == payload.room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    if payload.start_date > payload.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid pricing date range",
        )

    rule = PricingRule(
        room_id=payload.room_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        price=payload.price,
        name=payload.name,
    )

    db.add(rule)
    db.commit()
    db.refresh(rule)

    return rule


@router.put(
    "/{rule_id}",
    response_model=PricingOut,
    summary="Update pricing rule (admin)",
)
def update_pricing_rule(
    rule_id: int,
    payload: PricingUpdate,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    rule = db.query(PricingRule).filter(PricingRule.id == rule_id).first()
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pricing rule not found",
        )

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(rule, field, value)

    db.commit()
    db.refresh(rule)

    return rule


@router.delete(
    "/{rule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete pricing rule (admin)",
)
def delete_pricing_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    rule = db.query(PricingRule).filter(PricingRule.id == rule_id).first()
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pricing rule not found",
        )

    db.delete(rule)
    db.commit()

    return None
