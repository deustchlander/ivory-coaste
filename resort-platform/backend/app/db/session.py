from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

# -------------------------------------------------
# Engine
# -------------------------------------------------

engine = create_engine(
    settings.get_database_url(),
    pool_pre_ping=True,
)

# -------------------------------------------------
# Session factory
# -------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# -------------------------------------------------
# Dependency
# -------------------------------------------------

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a SQLAlchemy session
    and ensures proper cleanup.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
