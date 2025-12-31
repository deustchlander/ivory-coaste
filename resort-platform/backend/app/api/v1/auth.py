from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.guest import Guest
from app.schemas.guest import GuestCreate, GuestOut

router = APIRouter()

# -------------------------------------------------
# Security configuration
# -------------------------------------------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

ALGORITHM = "HS256"


# -------------------------------------------------
# Utility functions
# -------------------------------------------------

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {
        "exp": expire,
        "sub": subject,
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(db: Session, email: str, password: str) -> Optional[Guest]:
    user = db.query(Guest).filter(Guest.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Guest:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(Guest).filter(Guest.email == email).first()
    if user is None:
        raise credentials_exception

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    return user


# -------------------------------------------------
# API Endpoints
# -------------------------------------------------

@router.post("/login", summary="Admin login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(subject=user.email)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post(
    "/register-admin",
    response_model=GuestOut,
    summary="Create admin account (one-time setup)",
)
def register_admin(
    payload: GuestCreate,
    db: Session = Depends(get_db),
):
    """
    Creates an admin user.
    This endpoint should be disabled after initial setup.
    """
    existing = db.query(Guest).filter(Guest.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = Guest(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=get_password_hash(payload.password),
        is_admin=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get(
    "/me",
    response_model=GuestOut,
    summary="Get current admin profile",
)
def read_current_user(
    current_user: Guest = Depends(get_current_user),
):
    return current_user
