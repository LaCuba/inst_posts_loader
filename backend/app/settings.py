from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


# BASE_DIR = Path(__file__).resolve().parent.parent
# ENV_PATH = BASE_DIR.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env", env_file_encoding="utf-8")

    ENV: str

    DATABASE_URL: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_URL: str = "redis://localhost:6379/0"


settings = Settings()
