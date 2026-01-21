from datetime import datetime, timedelta
from argon2 import PasswordHasher
from jose import jwt
from core.config import settings

# Inicializar Argon2
ph = PasswordHasher()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def hash_password(password: str) -> str:
    """Genera un hash Argon2 seguro."""
    return ph.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verifica una contraseña usando Argon2."""
    try:
        return ph.verify(hashed_password, password)
    except Exception:
        return False


def create_access_token(data: dict) -> str:
    """Genera un JWT de acceso con expiración."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)