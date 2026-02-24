import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field


class BaseAppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    BASE_DIR: Path = Path(__file__).parent.parent
    ENVIRONMENT: str = "local"
    API_V1_PREFIX: str = "/api/v1"

    @property
    def DATABASE_URL(self) -> str:
        return f"sqlite+aiosqlite:///{self.BASE_DIR}/postgres_db"

class Settings(BaseAppSettings):
    ENVIRONMENT: str = "docker"

    POSTGRES_USER: Optional[str] = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: Optional[str] = os.getenv("POSTGRES_HOST")
    POSTGRES_DB_PORT: int = 5432
    POSTGRES_DB: Optional[str] = os.getenv("POSTGRES_DB")

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}"
            f":{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}"
            f":{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB}"
        )

