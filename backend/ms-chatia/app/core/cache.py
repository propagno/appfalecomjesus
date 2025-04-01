"""
Serviço de cache do sistema FaleComJesus.

Este módulo implementa o sistema de cache da aplicação,
incluindo cache distribuído com Redis e cache local em memória.

Features:
    - Cache distribuído Redis
    - Cache local em memória
    - Cache de sessões
    - Cache de respostas IA
    - Cache de versículos
    - Cache de planos
"""

from typing import Any, Dict, Optional, Union
from datetime import datetime, timedelta
import json
from redis import asyncio as aioredis
from .config import settings
from .logger import logger


class CacheManager:
    """
    Gerenciador de cache.

    Features:
        - Cache distribuído
        - Cache local
        - Sessões
        - Respostas IA
        - Versículos
        - Planos

    Attributes:
        redis_client: Cliente Redis
        local_cache: Cache local
        metrics: Métricas de cache
    """

    def __init__(
        self,
        redis_url: Optional[str] = None,
        local_size: int = 1000
    ):
        """
        Inicializa o gerenciador.

        Args:
            redis_url: URL do Redis
            local_size: Tamanho do cache local
        """
        # Redis
        self.redis_client = aioredis.from_url(
            redis_url or settings.redis_url,
            decode_responses=True
        )

        # Cache local
        self.local_cache = {}
        self.local_size = local_size

        # Métricas
        self.metrics = {
            "hits": 0,
            "misses": 0,
            "errors": 0
        }

    async def get(
        self,
        key: str,
        use_local: bool = True
    ) -> Optional[Any]:
        """
        Obtém valor do cache.

        Args:
            key: Chave
            use_local: Usar cache local

        Returns:
            Any: Valor ou None
        """
        try:
            # Cache local
            if use_local and key in self.local_cache:
                self.metrics["hits"] += 1
                return self.local_cache[key]

            # Redis
            value = await self.redis_client.get(key)

            if value:
                self.metrics["hits"] += 1
                # Atualiza local
                if use_local:
                    self._update_local(key, value)
                return json.loads(value)

            self.metrics["misses"] += 1
            return None

        except Exception as e:
            self.metrics["errors"] += 1
            logger.error(f"Erro ao obter cache: {str(e)}")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None,
        use_local: bool = True
    ) -> bool:
        """
        Define valor no cache.

        Args:
            key: Chave
            value: Valor
            expire: Tempo de expiração
            use_local: Usar cache local

        Returns:
            bool: True se sucesso
        """
        try:
            # Serializa
            data = json.dumps(value)

            # Redis
            await self.redis_client.set(
                key,
                data,
                ex=expire
            )

            # Cache local
            if use_local:
                self._update_local(key, value)

            return True

        except Exception as e:
            self.metrics["errors"] += 1
            logger.error(f"Erro ao definir cache: {str(e)}")
            return False

    async def delete(
        self,
        key: str,
        use_local: bool = True
    ) -> bool:
        """
        Remove valor do cache.

        Args:
            key: Chave
            use_local: Usar cache local

        Returns:
            bool: True se sucesso
        """
        try:
            # Redis
            await self.redis_client.delete(key)

            # Cache local
            if use_local and key in self.local_cache:
                del self.local_cache[key]

            return True

        except Exception as e:
            self.metrics["errors"] += 1
            logger.error(f"Erro ao remover cache: {str(e)}")
            return False

    async def get_session(
        self,
        session_id: str
    ) -> Optional[Dict]:
        """
        Obtém sessão.

        Args:
            session_id: ID da sessão

        Returns:
            Dict: Dados da sessão
        """
        try:
            # Busca
            data = await self.get(f"session:{session_id}")

            if data:
                # Verifica expiração
                if datetime.fromisoformat(data["expires_at"]) < datetime.utcnow():
                    await self.delete_session(session_id)
                    return None

                return data

            return None

        except Exception as e:
            logger.error(f"Erro ao obter sessão: {str(e)}")
            return None

    async def save_session(
        self,
        session_id: str,
        data: Dict,
        expire: int = 3600
    ) -> bool:
        """
        Salva sessão.

        Args:
            session_id: ID da sessão
            data: Dados
            expire: Tempo de expiração

        Returns:
            bool: True se sucesso
        """
        try:
            # Adiciona expiração
            data["expires_at"] = (
                datetime.utcnow() + timedelta(seconds=expire)
            ).isoformat()

            # Salva
            return await self.set(
                f"session:{session_id}",
                data,
                expire=expire
            )

        except Exception as e:
            logger.error(f"Erro ao salvar sessão: {str(e)}")
            return False

    async def delete_session(
        self,
        session_id: str
    ) -> bool:
        """
        Remove sessão.

        Args:
            session_id: ID da sessão

        Returns:
            bool: True se sucesso
        """
        try:
            return await self.delete(f"session:{session_id}")

        except Exception as e:
            logger.error(f"Erro ao remover sessão: {str(e)}")
            return False

    async def get_ai_response(
        self,
        prompt: str
    ) -> Optional[str]:
        """
        Obtém resposta da IA do cache.

        Args:
            prompt: Prompt

        Returns:
            str: Resposta ou None
        """
        try:
            return await self.get(f"ai_response:{prompt}")

        except Exception as e:
            logger.error(f"Erro ao obter resposta IA: {str(e)}")
            return None

    async def save_ai_response(
        self,
        prompt: str,
        response: str,
        expire: int = 3600
    ) -> bool:
        """
        Salva resposta da IA no cache.

        Args:
            prompt: Prompt
            response: Resposta
            expire: Tempo de expiração

        Returns:
            bool: True se sucesso
        """
        try:
            return await self.set(
                f"ai_response:{prompt}",
                response,
                expire=expire
            )

        except Exception as e:
            logger.error(f"Erro ao salvar resposta IA: {str(e)}")
            return False

    def _update_local(
        self,
        key: str,
        value: Any
    ) -> None:
        """
        Atualiza cache local.

        Args:
            key: Chave
            value: Valor
        """
        try:
            # Remove mais antigo se cheio
            if len(self.local_cache) >= self.local_size:
                self.local_cache.pop(next(iter(self.local_cache)))

            # Adiciona
            self.local_cache[key] = value

        except Exception as e:
            logger.error(f"Erro ao atualizar cache local: {str(e)}")

    def get_metrics(self) -> Dict:
        """
        Retorna métricas de cache.

        Returns:
            Dict: Métricas
        """
        return self.metrics.copy()

    async def close(self) -> None:
        """
        Fecha conexões.
        """
        try:
            await self.redis_client.close()

        except Exception as e:
            logger.error(f"Erro ao fechar cache: {str(e)}")


class ChatCache:
    """
    Cache específico para mensagens de chat.

    Permite armazenar e recuperar respostas baseadas em mensagens similares,
    otimizando o uso da API da OpenAI e melhorando o tempo de resposta.

    Features:
        - Cache de respostas por mensagem e usuário
        - Busca por similaridade
        - Controle de TTL
    """

    def __init__(self):
        """
        Inicializa o cache de chat.
        """
        self.cache_manager = cache

    async def get_cached_response(self, user_id: str, message: str):
        """
        Busca uma resposta em cache para a mensagem.

        Args:
            user_id: ID do usuário
            message: Mensagem do usuário

        Returns:
            Dict: Resposta em cache ou None
        """
        try:
            # Chave do cache
            cache_key = f"chat:user:{user_id}:msg:{hash(message.lower())}"

            # Busca no cache
            return await self.cache_manager.get(cache_key)
        except Exception as e:
            # Log do erro
            print(f"Erro ao buscar cache de chat: {str(e)}")
            return None

    async def cache_response(self, user_id: str, message: str, response):
        """
        Armazena uma resposta em cache.

        Args:
            user_id: ID do usuário
            message: Mensagem do usuário
            response: Resposta da IA

        Returns:
            bool: True se sucesso
        """
        try:
            # Chave do cache
            cache_key = f"chat:user:{user_id}:msg:{hash(message.lower())}"

            # Salva no cache
            return await self.cache_manager.set(
                cache_key,
                response,
                expire=3600  # 1 hora
            )
        except Exception as e:
            # Log do erro
            print(f"Erro ao salvar cache de chat: {str(e)}")
            return False


# Instância global de cache
cache = CacheManager()
