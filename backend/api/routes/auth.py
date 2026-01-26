from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from db.session import get_db
from models.user import User
from core.security import verify_password, get_password_hash, create_access_token
from dependencies.dependencies import current_user  # <-- IMPORTANTE

router = APIRouter(prefix="/auth", tags=["auth"])


# -----------------------------
# Pydantic Schemas
# -----------------------------
class RegisterRequest(BaseModel):
    email: str
    password: str


class RegisterResponse(BaseModel):
    id: int
    email: str
    created_at: datetime


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# -----------------------------
# Register
# -----------------------------
@router.post("/register", response_model=RegisterResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed = get_password_hash(payload.password)

    user = User(
        email=payload.email,
        hashed_password=hashed,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return RegisterResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at
    )


# -----------------------------
# Login
# -----------------------------
@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token(subject=str(user.id))

    return LoginResponse(access_token=token)


# -----------------------------
# Get current authenticated user
# -----------------------------
@router.get("/me")
def get_me(user: User = Depends(current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "role": getattr(user, "role", "viewer")
    }
