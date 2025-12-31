from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.room import Room
from app.models.pricing import PricingRule


def calculate_total_price(
    db: Session,
    room_id: int,
    check_in: date,
    check_out: date,
) -> Decimal:
    """
    Calculate total price for a room over a date range
    using base price + pricing rules.
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise ValueError("Room not found")

    rules = (
        db.query(PricingRule)
        .filter(PricingRule.room_id == room_id)
        .all()
    )

    total = Decimal("0.00")
    current_date = check_in

    while current_date < check_out:
        daily_price = room.base_price

        for rule in rules:
            if rule.start_date <= current_date <= rule.end_date:
                daily_price = rule.price
                break

        total += daily_price
        current_date += timedelta(days=1)

    return total
