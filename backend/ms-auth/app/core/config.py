import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Application settings
    debug: bool = Field(default=False)
    environment: str = Field(default="development")

    # Security settings
    secret_key: str = Field(default="dev_secret_key")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=15)  # 15 minutes
    refresh_token_expire_days: int = Field(default=7)  # 7 days

    # Database settings
    database_url: str = Field(
        env="DATABASE_URL",
        default="postgresql://postgres:postgres@auth-db:5432/auth")

    # CORS settings
    cors_origins_str: str = Field(default="http://localhost")

    # Redis settings (for caching and sessions)
    redis_url: str = Field(default="redis://redis:6379/0")

    # Microservice communication
    ms_study_url: str = Field(default="http://ms-study:8004")
    service_api_key: str = Field(default="internal_service_key")

    # Pydantic V2 configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"
    )

    def get_cors_origins(self) -> list:
        return self.cors_origins_str.split(",")


@lru_cache()
def get_settings():
    return Settings()
