from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8")

    # Database
    DATABASE_URL: str  # e.g., "postgresql+asyncpg://user:pass@localhost/dbname"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"


settings = Settings()
