import os
import secrets
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, validator, field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Base settings
    APP_NAME: str = "MS-Study"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ms-study"
    VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Database settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "study_db"
    POSTGRES_HOST: str = "study-db"
    POSTGRES_PORT: str = "5432"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None

    # Authentication settings
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # Microservices URLs
    MS_CHATIA_URL: str = "http://ms-chatia:5000"
    MS_AUTH_URL: str = "http://ms-auth:5000"

    # Service API Key for inter-service communication
    SERVICE_API_KEY: str = "your-service-api-key"

    # CORS settings como uma string simples
    CORS_ORIGINS: List[str] = ["*"]

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"

    # Pydantic V2 usa model_config em vez de Config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost",
        "http://localhost:8080",
    ]

    @field_validator("BACKEND_CORS_ORIGINS")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @field_validator("SQLALCHEMY_DATABASE_URI")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: Any) -> str:
        if v is not None:
            return v

        # Pega os valores do objeto de configuração atual
        values = info.data

        return f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_HOST')}:{values.get('POSTGRES_PORT')}/{values.get('POSTGRES_DB')}"

    # Integração com o MS-Auth
    AUTH_SERVICE_URL: str = "http://ms-auth:5000/api/v1"
    AUTH_SERVICE_VERIFY_TOKEN_URL: str = "/api/auth/verify-token"
    SERVICE_AUTH_KEY: str = os.getenv("SERVICE_AUTH_KEY", "secret-service-key")

    # Configuração para armazenamento de certificados
    CERTIFICATES_STORAGE_PATH: str = "/app/storage/certificates"
    CERTIFICATE_PUBLIC_URL: str = os.getenv(
        "CERTIFICATE_PUBLIC_URL", "https://falecomjesus.com/certificates")

    # Configurações de logging
    LOG_LEVEL: str = "INFO"

    # OpenAI
    OPENAI_API_KEY: Optional[str] = None

    # Docker
    DOCKER_IMAGE_MS_STUDY: str = "ms-study"

    # Certificados
    CERTIFICATE_TEMPLATE_PATH: str = "./app/templates/certificate_template.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def get_cors_origins(self) -> List[str]:
        return self.CORS_ORIGINS


# Instância global das configurações
settings = Settings()


@lru_cache()
def get_settings():
    """Return cached settings."""
    return settings
