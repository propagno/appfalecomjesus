import os
from typing import List, Optional, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, validator, Field
import secrets


class Settings(BaseSettings):
    """Configurações da aplicação."""
    PROJECT_NAME: str = "MS-Monetization"
    API_V1_STR: str = "/api/v1"

    # Ambiente
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 5000

    # Banco de dados
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "monetization"
    DATABASE_URI: Optional[str] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        return f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_HOST')}:{values.get('POSTGRES_PORT')}/{values.get('POSTGRES_DB')}"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0

    # Segurança
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # CORS - Lista fixa de origens permitidas
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000"

    # Integração com outros serviços
    MS_AUTH_URL: str = "http://localhost:8001/api/v1"
    MS_GAMIFICATION_URL: str = "http://localhost:8004/api/v1"
    MS_CHATIA_URL: str = "http://localhost:8002/api/v1"

    # Stripe
    STRIPE_API_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_MONTHLY_PRICE_ID: str = None
    STRIPE_YEARLY_PRICE_ID: str = None

    # Hotmart
    HOTMART_CLIENT_ID: Optional[str] = None
    HOTMART_CLIENT_SECRET: Optional[str] = None
    HOTMART_BASIC_AUTH: str = None
    HOTMART_API_URL: str = "https://sandbox.hotmart.com"
    HOTMART_WEBHOOK_SECRET: str = ""

    # Limites de uso
    MAX_DAILY_AD_REWARDS: int = 3  # Número máximo de recompensas por anúncios por dia

    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10

    # Service URLs
    AUTH_SERVICE_URL: str = "http://ms-auth:5000"
    STUDY_SERVICE_URL: str = "http://ms-study:5000"

    # API Settings
    APP_NAME: str = "ms-monetization"
    API_PREFIX: str = "/api/monetization"
    VERSION: str = "1.0.0"

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # JWT
    JWT_SECRET_KEY: str = "supersecretkey"

    # Stripe
    STRIPE_PUBLIC_KEY: str = "pk_test_your_stripe_public_key"
    STRIPE_SECRET_KEY: str = "sk_test_your_stripe_secret_key"

    # Hotmart
    HOTMART_APP_TOKEN: str = "your_hotmart_app_token"
    HOTMART_VALIDATE_WEBHOOK: bool = True

    # Service URLs
    CHATIA_SERVICE_URL: str = "http://ms-chatia:5000"

    # Chat Limits
    DEFAULT_CHAT_MESSAGES_LIMIT: int = 5

    # Service API Key
    SERVICE_API_KEY: str = "internal_service_key"

    def get_cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, env_nested_delimiter="__")


settings = Settings()
