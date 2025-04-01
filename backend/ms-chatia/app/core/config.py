"""
Serviço de configuração do sistema FaleComJesus.

Este módulo implementa o sistema de configuração da aplicação,
incluindo variáveis de ambiente, validações e valores padrão.

Features:
    - Configurações de ambiente
    - Configurações de banco
    - Configurações de cache
    - Configurações de segurança
    - Configurações de IA
    - Configurações de email
"""

from typing import Dict, List, Optional, Union, Any
import logging
import os
from pydantic_settings import BaseSettings
from pydantic import Field

# Logger
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """
    Configurações da aplicação.
    """

    # Ambiente
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    APP_NAME: str = "MS-ChatIA"
    APP_VERSION: str = "1.0.0"
    SECRET_KEY: str = "dev_secret_key_change_in_production"

    # JWT
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_SECRET_KEY: str = Field(
        default="dev_jwt_secret_key", alias="JWT_SECRET_KEY")

    # Banco
    DATABASE_URL: str = "postgresql://postgres:postgres@postgres:5432/falecomjesus"

    @property
    def database_url(self) -> str:
        """
        Retorna a URL do banco minúscula como alias para DATABASE_URL.

        Returns:
            str: URL do banco de dados
        """
        return self.DATABASE_URL

    # CORS
    CORS_ORIGINS_STR: str = "http://localhost,http://localhost:3000,https://falecomjesus.com"

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    REDIS_CHAT_DB: int = 0
    REDIS_RATE_LIMIT_DB: int = 1

    @property
    def redis_url(self) -> str:
        """
        Retorna a URL do Redis minúscula como alias para REDIS_URL.

        Returns:
            str: URL do Redis
        """
        return self.REDIS_URL

    # Chat
    CHAT_LIMIT_FREE_USERS: int = 5
    CHAT_LIMIT_MAX_BONUS: int = 20
    CHAT_LIMIT_KEY_TTL: int = 86400
    CHAT_BONUS_PER_AD: int = 5
    CHAT_HISTORY_MAX_ITEMS: int = 50

    # OpenAI
    OPENAI_API_KEY: str = "your_api_key_here"
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 800
    OPENAI_TIMEOUT: int = 30
    OPENAI_RETRY_ATTEMPTS: int = 3

    # Cache
    CACHE_TTL_BIBLE_VERSES: int = 3600
    CACHE_TTL_SUGGESTIONS: int = 1800

    # Microsserviços
    MS_AUTH_URL: str = "http://ms-auth:8002"
    MS_MONETIZATION_URL: str = "http://ms-monetization:8005"
    MS_BIBLE_URL: str = "http://ms-bible:8006"
    SERVICE_API_KEY: str = "internal-service-key-change-in-production"

    # Monitoramento
    APM_SERVER_URL: str = "http://apm:8200"
    ENABLE_METRICS: bool = True
    METRICS_PREFIX: str = "ms_chatia"
    elastic_url: str = "http://elasticsearch:9200"

    # Modo emergência
    EMERGENCY_MODE_ENABLED: bool = True
    EMERGENCY_MODE_TIMEOUT: int = 5

    @property
    def CORS_ORIGINS(self) -> List[str]:
        """
        Retorna as origens CORS.

        Returns:
            List[str]: Lista de origens CORS
        """
        return self.CORS_ORIGINS_STR.split(",")

    class Config:
        """
        Configuração do Pydantic.
        """
        env_file = ".env"
        case_sensitive = True


# Instância global de configurações
settings = Settings()

# Função para obter as configurações


def get_settings():
    """
    Retorna a instância global de configurações.

    Returns:
        Settings: Configurações da aplicação
    """
    return settings
