import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from uuid import UUID

import redis
from fastapi import HTTPException, status

from app.core.config import settings

logger = logging.getLogger(__name__)


class CacheService:
    """
    Serviço para gerenciamento de cache.

    Responsável por:
    - Armazenar dados temporários
    - Controlar limites de uso
    - Otimizar respostas frequentes
    - Gerenciar TTL de chaves

    Attributes:
        redis: Cliente Redis
        prefix: Prefixo para chaves
    """

    def __init__(self):
        """
        Inicializa o serviço de cache.

        Configura conexão com Redis.
        """
        self.redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        self.prefix = "fcj:"

    async def get(
        self,
        key: str
    ) -> Optional[str]:
        """
        Retorna valor do cache.

        Args:
            key: Chave do cache

        Returns:
            Valor ou None se não existe

        Raises:
            HTTPException: Se erro no Redis
        """
        try:
            full_key = f"{self.prefix}{key}"
            return self.redis.get(full_key)

        except redis.RedisError as e:
            logger.error(f"Redis error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao acessar cache"
            )

    async def set(
        self,
        key: str,
        value: str,
        ttl: Optional[int] = None
    ) -> None:
        """
        Salva valor no cache.

        Args:
            key: Chave do cache
            value: Valor a salvar
            ttl: Tempo de vida em segundos

        Raises:
            HTTPException: Se erro no Redis
        """
        try:
            full_key = f"{self.prefix}{key}"
            if ttl:
                self.redis.setex(full_key, ttl, value)
            else:
                self.redis.set(full_key, value)

        except redis.RedisError as e:
            logger.error(f"Redis error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao salvar no cache"
            )

    async def delete(
        self,
        key: str
    ) -> None:
        """
        Remove chave do cache.

        Args:
            key: Chave do cache

        Raises:
            HTTPException: Se erro no Redis
        """
        try:
            full_key = f"{self.prefix}{key}"
            self.redis.delete(full_key)

        except redis.RedisError as e:
            logger.error(f"Redis error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao remover do cache"
            )

    async def increment(
        self,
        key: str,
        amount: int = 1
    ) -> int:
        """
        Incrementa contador.

        Args:
            key: Chave do contador
            amount: Valor a incrementar

        Returns:
            Novo valor do contador

        Raises:
            HTTPException: Se erro no Redis
        """
        try:
            full_key = f"{self.prefix}{key}"
            return self.redis.incr(full_key, amount)

        except redis.RedisError as e:
            logger.error(f"Redis error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao incrementar contador"
            )

    async def decrement(
        self,
        key: str,
        amount: int = 1
    ) -> int:
        """
        Decrementa contador.

        Args:
            key: Chave do contador
            amount: Valor a decrementar

        Returns:
            Novo valor do contador

        Raises:
            HTTPException: Se erro no Redis
        """
        try:
            full_key = f"{self.prefix}{key}"
            return self.redis.decr(full_key, amount)

        except redis.RedisError as e:
            logger.error(f"Redis error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao decrementar contador"
            )

    async def exists(
        self,
        key: str
    ) -> bool:
        """
        Verifica se chave existe.

        Args:
            key: Chave do cache

        Returns:
            True se existe

        Raises:
            HTTPException: Se erro no Redis
        """
        try:
            full_key = f"{self.prefix}{key}"
            return bool(self.redis.exists(full_key))

        except redis.RedisError as e:
            logger.error(f"Redis error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao verificar cache"
            )

    async def ttl(
        self,
        key: str
    ) -> int:
        """
        Retorna tempo restante.

        Args:
            key: Chave do cache

        Returns:
            Segundos restantes ou -1

        Raises:
            HTTPException: Se erro no Redis
        """
        try:
            full_key = f"{self.prefix}{key}"
            return self.redis.ttl(full_key)

        except redis.RedisError as e:
            logger.error(f"Redis error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao verificar TTL"
            )

    async def set_daily_limit(
        self,
        user_id: UUID,
        resource: str,
        limit: int
    ) -> None:
        """
        Define limite diário.

        Args:
            user_id: ID do usuário
            resource: Tipo do recurso
            limit: Limite diário

        Raises:
            HTTPException: Se erro no Redis
        """
        try:
            key = f"limit:{resource}:{user_id}"
            full_key = f"{self.prefix}{key}"

            # Calcula TTL até meia-noite
            now = datetime.utcnow()
            midnight = now.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            ) + timedelta(days=1)
            ttl = int((midnight - now).total_seconds())

            # Salva limite
            self.redis.setex(full_key, ttl, limit)

        except redis.RedisError as e:
            logger.error(f"Redis error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao definir limite"
            )

    async def check_daily_limit(
        self,
        user_id: UUID,
        resource: str
    ) -> bool:
        """
        Verifica limite diário.

        Args:
            user_id: ID do usuário
            resource: Tipo do recurso

        Returns:
            True se ainda tem limite

        Raises:
            HTTPException: Se erro no Redis
        """
        try:
            key = f"limit:{resource}:{user_id}"
            full_key = f"{self.prefix}{key}"

            # Verifica se existe
            if not await self.exists(key):
                return True

            # Verifica valor
            value = int(await self.get(key) or 0)
            return value > 0

        except redis.RedisError as e:
            logger.error(f"Redis error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao verificar limite"
            )

    async def consume_daily_limit(
        self,
        user_id: UUID,
        resource: str
    ) -> bool:
        """
        Consome uma unidade do limite.

        Args:
            user_id: ID do usuário
            resource: Tipo do recurso

        Returns:
            True se consumiu com sucesso

        Raises:
            HTTPException: Se erro no Redis
        """
        try:
            key = f"limit:{resource}:{user_id}"

            # Verifica limite
            if not await self.check_daily_limit(user_id, resource):
                return False

            # Decrementa contador
            await self.decrement(key)
            return True

        except redis.RedisError as e:
            logger.error(f"Redis error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao consumir limite"
            )
