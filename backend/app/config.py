from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App settings, read from environment variables or a .env file."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Momentum API"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://momentum:momentum@localhost:5433/momentum"
    # Separate database for pytest; created automatically and wiped every test run
    test_database_url: str = "postgresql+psycopg://momentum:momentum@localhost:5433/momentum_test"
    cors_origins: list[str] = ["http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
