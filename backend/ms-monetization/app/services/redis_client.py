import redis.asyncio as redis
import logging
from typing import Optional, Any, Union
import json


class RedisClient:
    """
    Cliente para interação com o Redis.
    Utilizado para cache, limites de uso e armazenamento temporário.
    """

    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis: Optional[redis.Redis] = None
        self.logger = logging.getLogger(__name__)

    async def connect(self) -> None:
        """
        Estabelece conexão com o Redis.
        """
        if self.redis is None:
            try:
                self.redis = redis.Redis.from_url(
                    self.redis_url,
                    encoding="utf-8",
                    decode_responses=True
                )
                self.logger.info("Conexão com Redis estabelecida com sucesso")
            except Exception as e:
                self.logger.error(f"Erro ao conectar ao Redis: {str(e)}")
                raise e

    async def disconnect(self) -> None:
        """
        Fecha a conexão com o Redis.
        """
        if self.redis:
            await self.redis.close()
            self.redis = None
            self.logger.info("Conexão com Redis encerrada")

    @property
    def connected(self) -> bool:
        """
        Verifica se está conectado ao Redis.
        """
        return self.redis is not None

    async def _ensure_connection(self) -> None:
        """
        Garante que existe uma conexão com o Redis.
        """
        if not self.connected:
            await self.connect()

    async def get(self, key: str) -> Any:
        """
        Recupera um valor do Redis pelo key.
        """
        await self._ensure_connection()
        try:
            value = await self.redis.get(key)
            if value and value.startswith("{") and value.endswith("}"):
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return value
        except Exception as e:
            self.logger.error(
                f"Erro ao obter valor no Redis para chave {key}: {str(e)}")
            return None

    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """
        Define um valor no Redis.

        Args:
            key: Chave para armazenar o valor.
            value: Valor a ser armazenado.
            expire: Tempo de expiração em segundos.

        Returns:
            bool: True se definido com sucesso, False caso contrário.
        """
        await self._ensure_connection()
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)

            result = await self.redis.set(key, value)
            if expire:
                await self.redis.expire(key, expire)
            return result
        except Exception as e:
            self.logger.error(
                f"Erro ao definir valor no Redis para chave {key}: {str(e)}")
            return False

    async def delete(self, key: str) -> int:
        """
        Remove um valor do Redis.

        Returns:
            int: Número de chaves excluídas.
        """
        await self._ensure_connection()
        try:
            return await self.redis.delete(key)
        except Exception as e:
            self.logger.error(
                f"Erro ao excluir chave {key} no Redis: {str(e)}")
            return 0

    async def increment(self, key: str, amount: int = 1) -> int:
        """
        Incrementa um contador no Redis.

        Args:
            key: Chave do contador.
            amount: Quantidade a incrementar.

        Returns:
            int: Novo valor do contador.
        """
        await self._ensure_connection()
        try:
            return await self.redis.incrby(key, amount)
        except Exception as e:
            self.logger.error(
                f"Erro ao incrementar contador {key} no Redis: {str(e)}")
            return 0

    async def decrement(self, key: str, amount: int = 1) -> int:
        """
        Decrementa um contador no Redis.

        Args:
            key: Chave do contador.
            amount: Quantidade a decrementar.

        Returns:
            int: Novo valor do contador.
        """
        await self._ensure_connection()
        try:
            return await self.redis.decrby(key, amount)
        except Exception as e:
            self.logger.error(
                f"Erro ao decrementar contador {key} no Redis: {str(e)}")
            return 0

    async def exists(self, key: str) -> bool:
        """
        Verifica se uma chave existe no Redis.

        Args:
            key: Chave a verificar.

        Returns:
            bool: True se existir, False caso contrário.
        """
        await self._ensure_connection()
        try:
            result = await self.redis.exists(key)
            return bool(result)
        except Exception as e:
            self.logger.error(
                f"Erro ao verificar existência da chave {key} no Redis: {str(e)}")
            return False
