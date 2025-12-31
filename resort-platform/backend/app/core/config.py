from typing import List
from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # -------------------------------------------------
    # Project metadata
    # -------------------------------------------------
    PROJECT_NAME: str = "Resort Backend API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # -------------------------------------------------
    # Security
    # -------------------------------------------------
    SECRET_KEY: str = Field(..., description="JWT secret key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # -------------------------------------------------
    # CORS
    # -------------------------------------------------
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # -------------------------------------------------
    # Database
    # -------------------------------------------------
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    DATABASE_URL: str | None = None

    # -------------------------------------------------
    # Environment
    # -------------------------------------------------
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    def get_database_url(self) -> str:
        """
        Returns the SQLAlchemy-compatible database URL.
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL

        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


# Singleton settings object
settings = Settings()
