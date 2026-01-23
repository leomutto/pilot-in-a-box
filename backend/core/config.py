from pydantic_settings import BaseSettings
from pathlib import Path

# Ruta absoluta al directorio raíz del backend dentro del contenedor
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Ruta absoluta al archivo .env real
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ENV_PATH
        env_file_encoding = "utf-8"

settings = Settings()