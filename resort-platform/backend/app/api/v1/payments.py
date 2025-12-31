from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.payment import Payment
from app.models.booking import Booking
from app.models.guest import Guest
from app.schemas.payment import (
    PaymentCreate,
    PaymentOut,
    PaymentUpdate,
)
from app.api.v1.auth import get_current_user

router = APIRouter()


# -------------------------------------------------
# Public Endpoints
# -------------------------------------------------

@router.post(
    "/",
    response_model=PaymentOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create payment for a booking",
)
def create_payment(
    payload: PaymentCreate,
    db: Session = Depends(get_db),
):
    booking = db.query(Booking).filter(Booking.id == payload.booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    if payload.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment amount must be greater than zero",
        )

    payment = Payment(
        booking_id=payload.booking_id,
        amount=payload.amount,
        method=payload.method,
        status="PENDING",
        reference_id=payload.reference_id,
        paid_at=None,
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


# -------------------------------------------------
# Admin Endpoints
# -------------------------------------------------

@router.get(
    "/",
    response_model=List[PaymentOut],
    summary="List all payments (admin)",
)
def list_payments(
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    return (
        db.query(Payment)
        .order_by(Payment.created_at.desc())
        .all()
    )


@router.get(
    "/{payment_id}",
    response_model=PaymentOut,
    summary="Get payment by ID (admin)",
)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )
    return payment


@router.put(
    "/{payment_id}",
    response_model=PaymentOut,
    summary="Update payment status (admin)",
)
def update_payment(
    payment_id: int,
    payload: PaymentUpdate,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )

    data = payload.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(payment, field, value)

    if data.get("status") == "PAID":
        payment.paid_at = datetime.utcnow()

    db.commit()
    db.refresh(payment)

    return payment


@router.delete(
    "/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete payment record (admin)",
)
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: Guest = Depends(get_current_user),
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )

    db.delete(payment)
    db.commit()

    return None
