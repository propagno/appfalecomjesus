import redis.asyncio as redis
from typing import Optional, Any
import logging

from app.core.config import settings

# Configurar logger
logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self, url: Optional[str] = None):
        """Inicializa a conexão com o Redis."""
        self.redis_url = url or settings.REDIS_URL
        self.redis = None
        self.connected = False

    async def connect(self) -> bool:
        """Estabelece a conexão com o Redis."""
        try:
            self.redis = await redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            self.connected = True
            logger.info("Conexão com Redis estabelecida com sucesso")
            return True
        except Exception as e:
            logger.error(f"Falha ao conectar ao Redis: {str(e)}")
            self.connected = False
            return False

    async def disconnect(self) -> None:
        """Fecha a conexão com o Redis."""
        if self.redis and self.connected:
            await self.redis.close()
            self.connected = False
            logger.info("Conexão com Redis fechada")

    async def _ensure_connection(self) -> None:
        """Garante que a conexão está ativa."""
        if not self.connected or not self.redis:
            await self.connect()

    async def set(self, key: str, value: Any) -> bool:
        """Define um valor no Redis."""
        try:
            await self._ensure_connection()
            await self.redis.set(key, value)
            return True
        except Exception as e:
            logger.error(f"Erro ao definir valor no Redis: {str(e)}")
            return False

    async def get(self, key: str) -> Optional[str]:
        """Recupera um valor do Redis."""
        try:
            await self._ensure_connection()
            return await self.redis.get(key)
        except Exception as e:
            logger.error(f"Erro ao recuperar valor do Redis: {str(e)}")
            return None

    async def delete(self, key: str) -> bool:
        """Remove um valor do Redis."""
        try:
            await self._ensure_connection()
            await self.redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Erro ao remover valor do Redis: {str(e)}")
            return False

    async def exists(self, key: str) -> bool:
        """Verifica se uma chave existe no Redis."""
        try:
            await self._ensure_connection()
            return await self.redis.exists(key) > 0
        except Exception as e:
            logger.error(f"Erro ao verificar existência no Redis: {str(e)}")
            return False

    async def setex(self, key: str, seconds: int, value: Any) -> bool:
        """Define um valor no Redis com expiração em segundos."""
        try:
            await self._ensure_connection()
            await self.redis.setex(key, seconds, value)
            return True
        except Exception as e:
            logger.error(
                f"Erro ao definir valor com expiração no Redis: {str(e)}")
            return False

    async def ttl(self, key: str) -> int:
        """Recupera o tempo restante de uma chave."""
        try:
            await self._ensure_connection()
            return await self.redis.ttl(key)
        except Exception as e:
            logger.error(f"Erro ao recuperar TTL do Redis: {str(e)}")
            return -2  # Valor padrão quando a chave não existe

    async def incrby(self, key: str, amount: int = 1) -> Optional[int]:
        """Incrementa um valor numérico no Redis."""
        try:
            await self._ensure_connection()
            return await self.redis.incrby(key, amount)
        except Exception as e:
            logger.error(f"Erro ao incrementar valor no Redis: {str(e)}")
            return None

    async def decrby(self, key: str, amount: int = 1) -> Optional[int]:
        """Decrementa um valor numérico no Redis."""
        try:
            await self._ensure_connection()
            return await self.redis.decrby(key, amount)
        except Exception as e:
            logger.error(f"Erro ao decrementar valor no Redis: {str(e)}")
            return None

    async def check_chat_limit(self, user_id: str) -> int:
        """
        Verifica o limite de mensagens do chat para um usuário.
        Retorna o número de mensagens ainda disponíveis.
        """
        try:
            await self._ensure_connection()

            chat_key = f"chat_limit:{user_id}"
            value = await self.redis.get(chat_key)

            # Se o valor existir, retorna-o
            if value is not None:
                try:
                    return int(value)
                except ValueError:
                    return 0

            # Se não existir, retorna 0 (não temos como saber o limite sem verificar a assinatura)
            return 0

        except Exception as e:
            logger.error(f"Erro ao verificar limite de chat: {str(e)}")
            return 0
