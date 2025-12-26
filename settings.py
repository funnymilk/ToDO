from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "ToDo App"
    DEBUG: bool = True

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    #DATABASE_URL_LOCAL: str | None = None
    YA_USER: Optional[str] = None
    YA_PASSWORD: Optional[str] = None
    LOGLEVEL: str = "INFO"

    #Settings JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TTL_MINUTES: int = 15
    REFRESH_TTL_DAYS: int = 14

    @property
    def db_url(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def refresh_ttl_days(self) -> int:
        """Compatibility alias used by existing code (lowercase attr)."""
        return self.REFRESH_TTL_DAYS


def get_settings() -> "Settings":
    """Dependency used by FastAPI endpoints and other helpers."""
    return Settings()

