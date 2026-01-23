from datetime import datetime, timedelta
from argon2 import PasswordHasher
from jose import jwt
from core.config import settings

# Inicializar Argon2
ph = PasswordHasher()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def get_password_hash(password: str) -> str:
    """Genera un hash Argon2 seguro."""
    return ph.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verifica una contraseña usando Argon2."""
    try:
        return ph.verify(hashed_password, password)
    except Exception:
        return False


def create_access_token(subject: str) -> str:
    """Genera un JWT estándar con claim 'sub'."""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)