from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

# -------------------------------------------------
# Password hashing
# -------------------------------------------------

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def get_password_hash(password: str) -> str:
    """
    Hash a plain-text password.
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain-text password against a hash.
    """
    return pwd_context.verify(plain_password, hashed_password)


# -------------------------------------------------
# JWT configuration
# -------------------------------------------------

ALGORITHM = "HS256"


def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a signed JWT access token.

    `subject` is typically the user email or user ID.
    """
    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.utcnow(),
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> str:
    """
    Decode and validate a JWT.
    Returns the subject if valid.
    Raises JWTError if invalid.
    """
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    subject: str | None = payload.get("sub")
    if subject is None:
        raise JWTError("Token subject missing")

    return subject
