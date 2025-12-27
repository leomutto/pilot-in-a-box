from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Pilot-in-a-Box"
    API_VERSION: str = "v1"

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 días

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()