from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    """
    pass


# -------------------------------------------------
# Import all models here so Alembic can detect them
# -------------------------------------------------

from app.models.guest import Guest  # noqa
from app.models.room import Room  # noqa
from app.models.booking import Booking  # noqa
from app.models.payment import Payment  # noqa
from app.models.pricing import PricingRule  # noqa
from app.models.review import Review  # noqa
from app.models.dining import DiningItem  # noqa
