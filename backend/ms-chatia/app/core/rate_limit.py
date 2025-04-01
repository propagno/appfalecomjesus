from datetime import datetime, timedelta
from typing import Dict, Optional, Union
import json
import logging
from dataclasses import dataclass

from fastapi import Request, HTTPException
from app.core.redis import get_redis_client
from app.core.config import get_settings
from app.core.logging import get_logger

# Configurações
settings = get_settings()
logger = get_logger()


@dataclass
class RateLimitData:
    """Dados de limite de requisições."""
    allowed: bool
    remaining: int
    reset_in: int
    retry_after: Optional[str] = None


class RateLimitMiddleware:
    """Middleware para controle de taxa de requisições."""

    def __init__(
        self,
        requests_per_minute: int = settings.RATE_LIMIT_PER_MINUTE,
        requests_per_hour: int = settings.RATE_LIMIT_PER_HOUR,
        whitelist_paths: list = None
    ):
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.whitelist_paths = whitelist_paths or [
            "/health",
            "/docs",
            "/openapi.json",
            "/metrics"
        ]
        self.redis = None

    async def init_redis(self):
        """Inicializa conexão com Redis."""
        if not self.redis:
            self.redis = await get_redis_client()

    def should_check_rate_limit(self, request: Request) -> bool:
        """Verifica se o path deve ser limitado."""
        return request.url.path not in self.whitelist_paths

    async def check_rate_limit(
        self,
        key: str,
        limit: int,
        window: int
    ) -> RateLimitData:
        """
        Verifica limite de requisições.

        Args:
            key: Chave Redis para o limite
            limit: Número máximo de requisições
            window: Janela de tempo em segundos

        Returns:
            RateLimitData com status do limite
        """
        current = await self.redis.get(key)

        if not current:
            await self.redis.setex(key, window, 1)
            return RateLimitData(
                allowed=True,
                remaining=limit - 1,
                reset_in=window
            )

        count = int(current)
        if count >= limit:
            retry_after = await self.redis.ttl(key)
            return RateLimitData(
                allowed=False,
                remaining=0,
                reset_in=retry_after,
                retry_after=f"{retry_after} seconds"
            )

        await self.redis.incr(key)
        ttl = await self.redis.ttl(key)

        return RateLimitData(
            allowed=True,
            remaining=limit - (count + 1),
            reset_in=ttl
        )

    async def __call__(self, request: Request, call_next):
        """
        Processa requisição aplicando limite de taxa.

        Args:
            request: Request FastAPI
            call_next: Handler da próxima etapa

        Returns:
            Response da requisição se permitida
        """
        if not self.should_check_rate_limit(request):
            return await call_next(request)

        await self.init_redis()

        # Identificação do cliente
        client_ip = request.client.host
        path = request.url.path
        user_agent = request.headers.get("User-Agent", "unknown")

        # Chaves para controle por minuto e hora
        minute_key = f"rate_limit:1m:{client_ip}:{path}"
        hour_key = f"rate_limit:1h:{client_ip}:{path}"

        # Verificar limites
        minute_limit = await self.check_rate_limit(
            minute_key,
            self.requests_per_minute,
            60  # 1 minuto
        )

        hour_limit = await self.check_rate_limit(
            hour_key,
            self.requests_per_hour,
            3600  # 1 hora
        )

        # Se excedeu algum limite
        if not (minute_limit.allowed and hour_limit.allowed):
            logger.warning(
                "rate_limit_exceeded",
                extra={
                    "client_ip": client_ip,
                    "path": path,
                    "user_agent": user_agent,
                    "minute_remaining": minute_limit.remaining,
                    "hour_remaining": hour_limit.remaining,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Too many requests",
                    "retry_after": (
                        minute_limit.retry_after
                        if not minute_limit.allowed
                        else hour_limit.retry_after
                    )
                }
            )

        # Adicionar headers de rate limit
        response = await call_next(request)
        response.headers["X-RateLimit-Limit-Minute"] = str(
            self.requests_per_minute)
        response.headers["X-RateLimit-Remaining-Minute"] = str(
            minute_limit.remaining)
        response.headers["X-RateLimit-Reset-Minute"] = str(
            minute_limit.reset_in)

        return response


class ChatRateLimiter:
    """Controle de limite de mensagens do chat."""

    def __init__(self, redis_client=None):
        """
        Args:
            redis_client: Cliente Redis opcional
        """
        self.redis = redis_client
        self.logger = get_logger()
        self.daily_limit = settings.CHAT_LIMIT_FREE_USERS
        self.bonus_limit = settings.CHAT_LIMIT_MAX_BONUS

    async def init_redis(self):
        """Inicializa conexão com Redis se necessário."""
        if not self.redis:
            self.redis = await get_redis_client()

    async def check_chat_limit(self, user_id: str) -> Dict[str, Union[bool, int]]:
        """
        Verifica limite de mensagens do usuário.

        Args:
            user_id: ID do usuário

        Returns:
            Dict com status do limite:
            - allowed: bool
            - remaining: int
            - reset_in: int (segundos)
            - can_watch_ad: bool
        """
        await self.init_redis()
        key = f"chat_limit:{user_id}"

        # Verificar limite atual
        current = await self.redis.get(key)

        if not current:
            # Criar novo limite
            limit_data = {
                "count": 0,
                "bonus_used": 0,
                "reset_at": (datetime.utcnow() + timedelta(days=1)).timestamp()
            }
            await self.redis.setex(
                key,
                86400,  # 24h
                json.dumps(limit_data)
            )
            return {
                "allowed": True,
                "remaining": self.daily_limit,
                "reset_in": 86400,
                "can_watch_ad": True
            }

        # Carregar dados
        limit_data = json.loads(current)
        count = limit_data["count"]
        bonus_used = limit_data.get("bonus_used", 0)
        reset_at = limit_data["reset_at"]

        # Verificar limite total (base + bônus)
        total_limit = self.daily_limit + bonus_used
        if count >= total_limit:
            self.logger.info(
                "chat_limit_exceeded",
                extra={
                    "user_id": user_id,
                    "count": count,
                    "bonus_used": bonus_used,
                    "reset_at": reset_at
                }
            )

            # Pode assistir ad se não atingiu limite de bônus
            can_watch_ad = bonus_used < self.bonus_limit

            return {
                "allowed": False,
                "remaining": 0,
                "reset_in": int(reset_at - datetime.utcnow().timestamp()),
                "can_watch_ad": can_watch_ad
            }

        # Incrementar contador
        limit_data["count"] = count + 1
        await self.redis.setex(
            key,
            int(reset_at - datetime.utcnow().timestamp()),
            json.dumps(limit_data)
        )

        return {
            "allowed": True,
            "remaining": total_limit - (count + 1),
            "reset_in": int(reset_at - datetime.utcnow().timestamp()),
            "can_watch_ad": bonus_used < self.bonus_limit
        }

    async def add_bonus_messages(
        self,
        user_id: str,
        bonus: int = settings.CHAT_BONUS_PER_AD
    ) -> Dict[str, Union[bool, int]]:
        """
        Adiciona mensagens bônus após visualização de anúncio.

        Args:
            user_id: ID do usuário
            bonus: Número de mensagens bônus

        Returns:
            Dict com novo status do limite
        """
        await self.init_redis()
        key = f"chat_limit:{user_id}"
        current = await self.redis.get(key)

        if not current:
            # Criar novo limite com bônus
            limit_data = {
                "count": 0,
                "bonus_used": bonus,
                "reset_at": (datetime.utcnow() + timedelta(days=1)).timestamp()
            }
        else:
            # Atualizar limite existente
            limit_data = json.loads(current)
            current_bonus = limit_data.get("bonus_used", 0)

            # Verificar limite máximo de bônus
            if current_bonus >= self.bonus_limit:
                return {
                    "success": False,
                    "error": "Maximum bonus limit reached",
                    "current_bonus": current_bonus,
                    "max_bonus": self.bonus_limit
                }

            # Adicionar bônus respeitando limite
            new_bonus = min(current_bonus + bonus, self.bonus_limit)
            limit_data["bonus_used"] = new_bonus

        # Salvar dados
        ttl = int(limit_data["reset_at"] - datetime.utcnow().timestamp())
        await self.redis.setex(key, ttl, json.dumps(limit_data))

        self.logger.info(
            "bonus_messages_added",
            extra={
                "user_id": user_id,
                "bonus": bonus,
                "total_bonus": limit_data["bonus_used"],
                "count": limit_data["count"]
            }
        )

        return {
            "success": True,
            "current_bonus": limit_data["bonus_used"],
            "remaining": (
                self.daily_limit +
                limit_data["bonus_used"] -
                limit_data["count"]
            ),
            "reset_in": ttl
        }

    async def reset_limits(self):
        """Reseta todos os limites (útil para testes)."""
        await self.init_redis()
        async for key in self.redis.scan_iter("chat_limit:*"):
            await self.redis.delete(key)
