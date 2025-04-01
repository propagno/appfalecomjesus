import redis
import logging
from typing import Optional, Any, Union
from datetime import timedelta
from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisService:
    """
    Serviço para gerenciar a conexão e operações com o Redis.
    Fornece métodos para operações comuns de cache e contadores.
    """

    def __init__(self):
        """Inicializa a conexão com o Redis usando as configurações do settings."""
        self.client = None
        try:
            self.client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True  # Retorna strings em vez de bytes
            )
            self.client.ping()  # Verifica se a conexão está funcionando
            logger.info("Conexão com o Redis estabelecida com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao conectar ao Redis: {str(e)}")
            self.client = None

    def get(self, key: str) -> Optional[str]:
        """
        Obtém um valor do Redis pelo nome da chave.

        Args:
            key: Nome da chave para buscar

        Returns:
            Valor armazenado ou None se não existir ou houver erro
        """
        if not self.client:
            logger.error("Cliente Redis não inicializado.")
            return None

        try:
            return self.client.get(key)
        except Exception as e:
            logger.error(f"Erro ao buscar chave {key} no Redis: {str(e)}")
            return None

    def set(self, key: str, value: str, expiry_seconds: Optional[int] = None) -> bool:
        """
        Define um valor no Redis com chave e tempo de expiração opcional.

        Args:
            key: Nome da chave
            value: Valor a ser armazenado
            expiry_seconds: Tempo de expiração em segundos (opcional)

        Returns:
            True se sucesso, False se falha
        """
        if not self.client:
            logger.error("Cliente Redis não inicializado.")
            return False

        try:
            if expiry_seconds is not None:
                return bool(self.client.setex(key, expiry_seconds, value))
            else:
                return bool(self.client.set(key, value))
        except Exception as e:
            logger.error(f"Erro ao definir chave {key} no Redis: {str(e)}")
            return False

    def delete(self, key: str) -> bool:
        """
        Remove uma chave do Redis.

        Args:
            key: Nome da chave a ser removida

        Returns:
            True se a chave foi removida, False caso contrário
        """
        if not self.client:
            logger.error("Cliente Redis não inicializado.")
            return False

        try:
            return bool(self.client.delete(key))
        except Exception as e:
            logger.error(f"Erro ao remover chave {key} do Redis: {str(e)}")
            return False

    def exists(self, key: str) -> bool:
        """
        Verifica se uma chave existe no Redis.

        Args:
            key: Nome da chave a verificar

        Returns:
            True se a chave existe, False caso contrário
        """
        if not self.client:
            logger.error("Cliente Redis não inicializado.")
            return False

        try:
            return bool(self.client.exists(key))
        except Exception as e:
            logger.error(
                f"Erro ao verificar existência da chave {key} no Redis: {str(e)}")
            return False

    def increment(self, key: str, amount: int = 1) -> int:
        """
        Incrementa um contador no Redis.

        Args:
            key: Nome da chave do contador
            amount: Quantidade a incrementar (padrão: 1)

        Returns:
            Novo valor do contador ou 0 se falhar
        """
        if not self.client:
            logger.error("Cliente Redis não inicializado.")
            return 0

        try:
            return int(self.client.incrby(key, amount))
        except Exception as e:
            logger.error(f"Erro ao incrementar chave {key} no Redis: {str(e)}")
            return 0

    def decrement(self, key: str, amount: int = 1) -> int:
        """
        Decrementa um contador no Redis.

        Args:
            key: Nome da chave do contador
            amount: Quantidade a decrementar (padrão: 1)

        Returns:
            Novo valor do contador ou 0 se falhar
        """
        if not self.client:
            logger.error("Cliente Redis não inicializado.")
            return 0

        try:
            return int(self.client.decrby(key, amount))
        except Exception as e:
            logger.error(f"Erro ao decrementar chave {key} no Redis: {str(e)}")
            return 0

    def set_with_ttl(self, key: str, value: str, expiry: Union[int, timedelta]) -> bool:
        """
        Define um valor no Redis com tempo de vida (TTL).

        Args:
            key: Nome da chave
            value: Valor a ser armazenado
            expiry: Tempo de expiração em segundos ou timedelta

        Returns:
            True se sucesso, False se falha
        """
        if not self.client:
            logger.error("Cliente Redis não inicializado.")
            return False

        try:
            seconds = expiry.total_seconds() if isinstance(expiry, timedelta) else expiry
            return bool(self.client.setex(key, int(seconds), value))
        except Exception as e:
            logger.error(
                f"Erro ao definir chave {key} com TTL no Redis: {str(e)}")
            return False

    def get_ttl(self, key: str) -> int:
        """
        Obtém o tempo restante de vida de uma chave no Redis.

        Args:
            key: Nome da chave

        Returns:
            Tempo em segundos, -1 se não tiver TTL, -2 se não existir, 0 em caso de erro
        """
        if not self.client:
            logger.error("Cliente Redis não inicializado.")
            return 0

        try:
            return self.client.ttl(key)
        except Exception as e:
            logger.error(
                f"Erro ao obter TTL da chave {key} no Redis: {str(e)}")
            return 0

    def set_chat_limit(self, user_id: str, limit: int, expiration: int = 86400) -> bool:
        """
        Define o limite de mensagens de chat para um usuário.

        Args:
            user_id: ID do usuário
            limit: Número de mensagens disponíveis
            expiration: Tempo de expiração em segundos (padrão: 1 dia)

        Returns:
            True se a operação for bem-sucedida, False caso contrário
        """
        key = f"chat_limit:{user_id}"
        return self.set(key, str(limit), expiration)

    def get_chat_limit(self, user_id: str) -> int:
        """
        Obtém o limite de mensagens de chat para um usuário.

        Args:
            user_id: ID do usuário

        Returns:
            Número de mensagens disponíveis ou 0 se limite não existir
        """
        key = f"chat_limit:{user_id}"
        value = self.get(key)
        return int(value) if value else 0

    def increment_chat_limit(self, user_id: str, amount: int = 5) -> Optional[int]:
        """
        Incrementa o limite de mensagens de chat para um usuário.

        Args:
            user_id: ID do usuário
            amount: Quantidade a incrementar (padrão: 5)

        Returns:
            Novo limite de mensagens ou None se falhar
        """
        key = f"chat_limit:{user_id}"
        if not self.exists(key):
            # Se não existe, criar com limite e expirar em 1 dia
            self.set_chat_limit(user_id, amount)
            return amount

        return self.increment(key, amount)

    def decrement_chat_limit(self, user_id: str) -> Optional[int]:
        """
        Decrementa o limite de mensagens de chat para um usuário.

        Args:
            user_id: ID do usuário

        Returns:
            Novo limite de mensagens ou None se falhar
        """
        key = f"chat_limit:{user_id}"
        if not self.exists(key):
            return 0

        return self.decrement(key)

    def has_chat_messages_available(self, user_id: str) -> bool:
        """
        Verifica se um usuário tem mensagens disponíveis.

        Args:
            user_id: ID do usuário

        Returns:
            True se o usuário tem mensagens disponíveis, False caso contrário
        """
        return self.get_chat_limit(user_id) > 0
