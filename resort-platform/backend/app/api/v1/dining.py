from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.dining import DiningItem
from app.schemas.dining import (
    DiningCreate,
    DiningOut,
    DiningUpdate,
)
from app.models.guest import Guest
from app.api.v1.auth import get_current_user

router = APIRouter()


# -------------------------------------------------
# Public Endpoints
# -------------------------------------------------

@router.get(
    "/",
    response_model=List[DiningOut],
    summary="List dining items and meal plans",
)
def list_dining_items(
    db: Session = Depends(get_db),
):
    """
    Public endpoint to fetch all dining items and meal plans.
    """
    return (
        db.query(DiningItem)
        .order_by(DiningItem.display_order.asc())
        .all()
    )


@router.get(
    "/{item_id}",
    response_model=DiningOut,
    summary="Get dining item by ID",
)
def get_dining_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    item = db.query(DiningItem).filter(DiningItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dining item not found",
        )
    return item


# -------------------------------------------------
# Admin Endpoints
# -------------------------------------------------

@router.post(
    "/",
    response_model=DiningOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create dining item (admin)",
)
def create_dining_item(
    payload: DiningCreate,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    item = DiningItem(
        name=payload.name,
        description=payload.description,
        meal_type=payload.meal_type,
        price=payload.price,
        is_vegetarian=payload.is_vegetarian,
        is_available=payload.is_available,
        display_order=payload.display_order,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


@router.put(
    "/{item_id}",
    response_model=DiningOut,
    summary="Update dining item (admin)",
)
def update_dining_item(
    item_id: int,
    payload: DiningUpdate,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    item = db.query(DiningItem).filter(DiningItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dining item not found",
        )

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)

    return item


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete dining item (admin)",
)
def delete_dining_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    item = db.query(DiningItem).filter(DiningItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dining item not found",
        )

    db.delete(item)
    db.commit()

    return None
