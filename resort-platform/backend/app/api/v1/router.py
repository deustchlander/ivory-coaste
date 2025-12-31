from fastapi import APIRouter

from app.api.v1 import (
    auth,
    rooms,
    bookings,
    pricing,
    payments,
    guests,
    reviews,
    dining,
)

api_router = APIRouter()

# ---------------------------------------
# Authentication
# ---------------------------------------
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)

# ---------------------------------------
# Rooms & Property
# ---------------------------------------
api_router.include_router(
    rooms.router,
    prefix="/rooms",
    tags=["Rooms"],
)

# ---------------------------------------
# Bookings & Availability
# ---------------------------------------
api_router.include_router(
    bookings.router,
    prefix="/bookings",
    tags=["Bookings"],
)

# ---------------------------------------
# Pricing & Offers
# ---------------------------------------
api_router.include_router(
    pricing.router,
    prefix="/pricing",
    tags=["Pricing"],
)

# ---------------------------------------
# Payments
# ---------------------------------------
api_router.include_router(
    payments.router,
    prefix="/payments",
    tags=["Payments"],
)

# ---------------------------------------
# Guests & CRM
# ---------------------------------------
api_router.include_router(
    guests.router,
    prefix="/guests",
    tags=["Guests"],
)

# ---------------------------------------
# Reviews & Testimonials
# ---------------------------------------
api_router.include_router(
    reviews.router,
    prefix="/reviews",
    tags=["Reviews"],
)

# ---------------------------------------
# Dining & Meal Plans
# ---------------------------------------
api_router.include_router(
    dining.router,
    prefix="/dining",
    tags=["Dining"],
)
