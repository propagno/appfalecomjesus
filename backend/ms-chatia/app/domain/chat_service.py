from typing import Dict, Any, List
from uuid import UUID
import logging
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.infrastructure.redis_client import get_redis_client
from app.infrastructure.openai_client import get_openai_response
from app.domain.models.chat import ChatMessage

# Configuração de logging
logger = logging.getLogger(__name__)


async def process_chat_message(
    user_id: UUID,
    message: str,
    db: Session,
    is_premium: bool = False
) -> Dict[str, Any]:
    """
    Processa uma mensagem de chat, verifica limites, obtém resposta da IA
    e salva no histórico.
    """
    settings = get_settings()

    # Para usuários não premium, verificar limites diários
    remaining_messages = None
    if not is_premium:
        # Verificar limite no Redis
        redis = await get_redis_client()
        limit_key = f"chat:limit:{user_id}"

        # Obter contagem atual, se existir
        remaining = await redis.get(limit_key)

        if remaining is None:
            # Primeiro uso do dia, definir limite
            remaining = settings.CHAT_LIMIT_FREE_USERS
            await redis.set(
                limit_key,
                remaining,
                ex=settings.CHAT_LIMIT_KEY_TTL
            )
        else:
            remaining = int(remaining)

        if remaining <= 0:
            return {
                "response": "Você atingiu seu limite diário de mensagens. Faça upgrade para o plano premium ou assista a um anúncio para continuar.",
                "remaining_messages": 0
            }

        # Decrementar contador
        remaining = await redis.decr(limit_key)
        remaining_messages = remaining

    # Processar mensagem com OpenAI
    ai_response = await get_openai_response(message)

    # Salvar no banco de dados
    chat_message = ChatMessage(
        user_id=str(user_id),
        message=message,
        response=ai_response,
        model_used=settings.OPENAI_MODEL
    )

    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)

    return {
        "response": ai_response,
        "remaining_messages": remaining_messages
    }


async def get_chat_history(
    user_id: UUID,
    db: Session,
    limit: int = 10,
    skip: int = 0
) -> Dict[str, Any]:
    """
    Obtém o histórico de chat do usuário
    """
    # Contar total de mensagens
    total_count = db.query(ChatMessage).filter(
        ChatMessage.user_id == str(user_id)
    ).count()

    # Obter mensagens paginadas
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == str(user_id)
    ).order_by(
        ChatMessage.created_at.desc()
    ).offset(skip).limit(limit).all()

    return {
        "items": messages,
        "count": total_count
    }


async def get_message_limit_info(user_id: UUID) -> Dict[str, Any]:
    """
    Obtém informações sobre o limite de mensagens do usuário
    """
    settings = get_settings()
    redis = await get_redis_client()

    limit_key = f"chat:limit:{user_id}"
    remaining = await redis.get(limit_key)
    ttl = await redis.ttl(limit_key)

    # Se não houver registro, significa que o usuário não utilizou o chat hoje
    if remaining is None:
        return {
            "remaining_messages": settings.CHAT_LIMIT_FREE_USERS,
            "limit": settings.CHAT_LIMIT_FREE_USERS,
            "reset_in": settings.CHAT_LIMIT_KEY_TTL
        }

    return {
        "remaining_messages": int(remaining),
        "limit": settings.CHAT_LIMIT_FREE_USERS,
        "reset_in": ttl
    }


async def add_bonus_messages(user_id: UUID, bonus: int = 5) -> int:
    """
    Adiciona mensagens bônus após assistir anúncio
    """
    settings = get_settings()
    redis = await get_redis_client()

    limit_key = f"chat:limit:{user_id}"
    remaining = await redis.get(limit_key)

    # Se não houver registro, criar um novo
    if remaining is None:
        new_remaining = settings.CHAT_LIMIT_FREE_USERS + bonus
        await redis.set(
            limit_key,
            new_remaining,
            ex=settings.CHAT_LIMIT_KEY_TTL
        )
        return new_remaining

    # Adicionar bônus ao contador existente
    new_remaining = await redis.incrby(limit_key, bonus)

    return new_remaining
