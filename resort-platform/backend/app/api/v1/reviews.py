from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.review import Review
from app.models.booking import Booking
from app.models.guest import Guest
from app.schemas.review import (
    ReviewCreate,
    ReviewOut,
    ReviewUpdate,
)
from app.api.v1.auth import get_current_user

router = APIRouter()


# -------------------------------------------------
# Public Endpoints
# -------------------------------------------------

@router.get(
    "/",
    response_model=List[ReviewOut],
    summary="List approved reviews",
)
def list_reviews(
    db: Session = Depends(get_db),
):
    """
    Returns only approved reviews for public display.
    """
    return (
        db.query(Review)
        .filter(Review.is_approved.is_(True))
        .order_by(Review.created_at.desc())
        .all()
    )


@router.post(
    "/",
    response_model=ReviewOut,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a review",
)
def create_review(
    payload: ReviewCreate,
    db: Session = Depends(get_db),
):
    """
    Public endpoint to submit a review.
    Reviews are unapproved by default and require admin moderation.
    """

    booking = db.query(Booking).filter(Booking.id == payload.booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    existing = (
        db.query(Review)
        .filter(Review.booking_id == payload.booking_id)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Review already submitted for this booking",
        )

    review = Review(
        booking_id=payload.booking_id,
        guest_name=payload.guest_name,
        rating=payload.rating,
        comment=payload.comment,
        is_approved=False,
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review


# -------------------------------------------------
# Admin Endpoints
# -------------------------------------------------

@router.get(
    "/admin",
    response_model=List[ReviewOut],
    summary="List all reviews (admin)",
)
def list_all_reviews(
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    return (
        db.query(Review)
        .order_by(Review.created_at.desc())
        .all()
    )


@router.put(
    "/{review_id}",
    response_model=ReviewOut,
    summary="Update or approve review (admin)",
)
def update_review(
    review_id: int,
    payload: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(review, field, value)

    db.commit()
    db.refresh(review)

    return review


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete review (admin)",
)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    db.delete(review)
    db.commit()

    return None
