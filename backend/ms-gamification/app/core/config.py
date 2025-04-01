import os
import secrets
from typing import Any, Dict, List, Optional, Union
from functools import lru_cache

from pydantic import AnyHttpUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Configurações da API
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    VERSION: str = "0.1.0"
    PROJECT_NAME: str = "MS-Gamification"

    # Configurações de ambiente
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    PORT: int = int(os.getenv("PORT", "8004"))

    # Frontend URL para CORS
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # Configurações do banco de dados
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "gamification")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    DB_URL: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", "DB_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        # Retornar uma string em vez de um objeto PostgresDsn
        return f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}:{values.get('POSTGRES_PORT')}/{values.get('POSTGRES_DB')}"

    # Configurações de autenticação
    AUTH_SERVICE_URL: str = os.getenv(
        "AUTH_SERVICE_URL", "http://ms-auth:8001")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 dias

    # URLs dos microsserviços
    MS_STUDY_URL: str = os.getenv("MS_STUDY_URL", "http://ms-study:8002")
    MS_CHATIA_URL: str = os.getenv("MS_CHATIA_URL", "http://ms-chatia:8003")

    # Configurações de cache (Redis)
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()


@lru_cache()
def get_settings() -> Settings:
    """Retorna uma instância das configurações cacheada para performance"""
    return settings
