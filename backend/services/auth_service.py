from sqlalchemy.orm import Session

from models.user import User
from core.security import verify_password, create_access_token


def authenticate_user(db: Session, email: str, password: str):
    """Devuelve el usuario si las credenciales son correctas, sino None."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def login(db: Session, email: str, password: str):
    """Autentica y genera token JWT."""
    user = authenticate_user(db, email, password)
    if not user:
        return None

    # JWT estándar: sub = user.id
    token = create_access_token(subject=str(user.id))

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
    }
