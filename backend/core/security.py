from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from argon2 import PasswordHasher
from jose import jwt, JWTError

from core.config import settings
from db.session import get_db
from models.user import User

# ---------------------------------------------------------
# Password hashing (Argon2)
# ---------------------------------------------------------
ph = PasswordHasher()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# HTTP Bearer para Authorization: Bearer <token>
security_scheme = HTTPBearer()


# ---------------------------------------------------------
# Password helpers
# ---------------------------------------------------------
def get_password_hash(password: str) -> str:
    return ph.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, password)
    except Exception:
        return False


# ---------------------------------------------------------
# JWT creation
# ---------------------------------------------------------
def create_access_token(subject: str, role: str = "viewer") -> str:
    """
    Genera un JWT estándar con:
    - sub: user id
    - role: rol lógico (viewer/admin)
    """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": subject,
        "role": role,
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ---------------------------------------------------------
# JWT validation (HTTPBearer)
# ---------------------------------------------------------
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db=Depends(get_db),
) -> User:
    """
    Valida el JWT recibido vía Authorization: Bearer <token>
    y retorna el usuario autenticado.
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[str] = payload.get("sub")
        role: str = payload.get("role", "viewer")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing subject",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Adjuntamos el rol al objeto user (no toca DB)
    user.role = role
    return user


# ---------------------------------------------------------
# Role-based access control
# ---------------------------------------------------------
def require_role(required_role: str):
    """
    Uso:
    @router.get(..., dependencies=[Depends(require_role("admin"))])
    """
    def role_checker(user: User = Depends(get_current_user)):
        if getattr(user, "role", "viewer") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User requires role '{required_role}'",
            )
        return user

    return role_checker
