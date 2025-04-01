from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
import logging
from datetime import datetime, timedelta

from app.dependencies import (
    get_current_user,
    get_redis_client,
    get_subscription_service
)
from app.infrastructure.redis_client import RedisClient
from app.services.subscription_service import SubscriptionService
from app.core.config import settings

# Configurar logger
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/chat-messages-remaining", response_model=int)
async def get_remaining_chat_messages(
    user_id: str = Depends(get_current_user),
    redis_client: RedisClient = Depends(get_redis_client),
    subscription_service: SubscriptionService = Depends(
        get_subscription_service)
):
    """
    Retorna o número de mensagens restantes para o usuário no dia atual.
    Usado pelo frontend para exibir o contador de mensagens e decidir se deve mostrar ads.
    """
    try:
        # Buscar na cache do Redis
        chat_key = f"chat_limit:{user_id}"
        count = await redis_client.get(chat_key)

        if count is not None:
            # Se já existe um valor no Redis, retorná-lo
            try:
                return int(count)
            except ValueError:
                # Se o valor não é um número, tratar como 0
                return 0

        # Se não existe, verificar o plano do usuário e definir o limite baseado no plano
        status = await subscription_service.get_subscription_status(user_id)
        is_premium = status.is_premium

        # Usuários premium têm mensagens ilimitadas (representadas por -1)
        if is_premium:
            # Não precisamos armazenar no Redis para premium
            return -1

        # Para usuários gratuitos, definir o limite padrão
        daily_limit = status.chat_messages_per_day

        # Calcular segundos até o final do dia para TTL do Redis
        now = datetime.utcnow()
        midnight = now.replace(hour=23, minute=59, second=59)
        seconds_until_midnight = int((midnight - now).total_seconds())

        # Salvar no Redis com TTL
        await redis_client.setex(chat_key, seconds_until_midnight, daily_limit)

        return daily_limit

    except Exception as e:
        logger.error(f"Erro ao verificar mensagens restantes: {str(e)}")
        # Em caso de erro, retornar valor padrão para não bloquear usuário
        return settings.DEFAULT_CHAT_MESSAGES_LIMIT


@router.post("/decrement-chat-limit", response_model=int)
async def decrement_chat_limit(
    user_id: str = Depends(get_current_user),
    redis_client: RedisClient = Depends(get_redis_client),
    subscription_service: SubscriptionService = Depends(
        get_subscription_service)
):
    """
    Decrementa o contador de mensagens restantes do usuário.
    Chamado quando o usuário envia uma mensagem no chat.
    """
    try:
        # Verificar se é usuário premium
        status = await subscription_service.get_subscription_status(user_id)
        is_premium = status.is_premium

        # Usuários premium têm mensagens ilimitadas
        if is_premium:
            return -1

        # Para usuários gratuitos, decrementar do Redis
        chat_key = f"chat_limit:{user_id}"

        # Verificar se a chave existe
        exists = await redis_client.exists(chat_key)

        if not exists:
            # Se não existe, configurar o valor inicial e então decrementar
            daily_limit = status.chat_messages_per_day

            # Calcular segundos até o final do dia para TTL
            now = datetime.utcnow()
            midnight = now.replace(hour=23, minute=59, second=59)
            seconds_until_midnight = int((midnight - now).total_seconds())

            # Definir o valor inicial no Redis
            await redis_client.setex(chat_key, seconds_until_midnight, daily_limit)

            # Decrementar
            value = await redis_client.decrby(chat_key, 1)
            return value if value is not None else daily_limit - 1

        # Se a chave existe, decrementar diretamente
        value = await redis_client.get(chat_key)

        # Verificar se ainda tem mensagens disponíveis
        try:
            remaining = int(value) if value is not None else 0
        except ValueError:
            remaining = 0

        if remaining <= 0:
            # Não há mais mensagens disponíveis
            return 0

        # Decrementar e retornar o novo valor
        new_value = await redis_client.decrby(chat_key, 1)
        return new_value if new_value is not None else max(0, remaining - 1)

    except Exception as e:
        logger.error(f"Erro ao decrementar limite de chat: {str(e)}")
        # Em caso de erro, retornar valor positivo baixo para não bloquear completamente
        return 1
