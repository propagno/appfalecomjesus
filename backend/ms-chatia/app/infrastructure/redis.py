import redis
from fastapi import Depends
from functools import lru_cache

from app.core.config import get_settings, Settings


@lru_cache()
def get_redis_client():
    """
    Creates and returns a Redis client instance.
    """
    settings = get_settings()
    client = redis.from_url(settings.redis_url, decode_responses=True)
    return client


async def get_chat_limit(user_id: str, settings: Settings = Depends(get_settings)):
    """
    Gets the remaining chat messages for a user.

    Args:
        user_id: The user's unique identifier
        settings: Application settings

    Returns:
        int: Number of remaining messages for the day
    """
    redis_client = get_redis_client()
    limit_key = f"chat_limit:{user_id}"

    # Try to get current limit value
    current_limit = redis_client.get(limit_key)

    # If key doesn't exist, set it with the default limit and TTL
    if current_limit is None:
        redis_client.setex(
            limit_key,
            settings.chat_limit_key_ttl,
            settings.chat_limit_free_users
        )
        return settings.chat_limit_free_users

    return int(current_limit)


async def decrement_chat_limit(user_id: str):
    """
    Decrements the chat limit counter for a user.

    Args:
        user_id: The user's unique identifier

    Returns:
        int: New number of remaining messages, or -1 if no messages left
    """
    redis_client = get_redis_client()
    limit_key = f"chat_limit:{user_id}"

    # Get the current limit
    current_limit = redis_client.get(limit_key)

    # If there's no limit set or it's 0, return -1
    if current_limit is None or int(current_limit) <= 0:
        return -1

    # Decrement the counter
    new_limit = redis_client.decr(limit_key)
    return new_limit


async def increment_chat_limit(user_id: str, amount: int = 5):
    """
    Adds additional chat messages to a user's limit after watching an ad.

    Args:
        user_id: The user's unique identifier
        amount: Number of messages to add (default: 5)

    Returns:
        int: New number of remaining messages
    """
    redis_client = get_redis_client()
    limit_key = f"chat_limit:{user_id}"

    # Get current limit
    current_limit = redis_client.get(limit_key)

    # If no limit exists, create it with the specified amount and TTL
    settings = get_settings()
    if current_limit is None:
        redis_client.setex(limit_key, settings.chat_limit_key_ttl, amount)
        return amount

    # Add to the existing limit
    new_limit = redis_client.incrby(limit_key, amount)

    # Make sure TTL is still set
    ttl = redis_client.ttl(limit_key)
    if ttl == -1:  # No expiration
        redis_client.expire(limit_key, settings.chat_limit_key_ttl)

    return new_limit


async def check_subscription_and_limit(user_id: str, subscription_type: str = "free"):
    """
    Verifica o tipo de assinatura do usuário e aplica os limites adequados.

    Args:
        user_id: O ID do usuário
        subscription_type: O tipo de assinatura ('free' ou 'premium')

    Returns:
        dict: Informações sobre o limite atual, incluindo:
            - remaining: número de mensagens restantes
            - is_limited: se o usuário está sujeito a limites
            - reset_time: tempo até o reset do limite
    """
    # Usuários premium não têm limite
    if subscription_type.lower() == "premium":
        return {
            "remaining": -1,  # -1 indica sem limite
            "is_limited": False,
            "reset_time": None
        }

    # Para usuários free, verificar o limite atual
    redis_client = get_redis_client()
    limit_key = f"chat_limit:{user_id}"

    # Tenta obter o valor atual do limite
    current_limit = redis_client.get(limit_key)

    # Obtém as configurações
    settings = get_settings()

    # Se não existir, define o limite padrão
    if current_limit is None:
        redis_client.setex(
            limit_key,
            settings.chat_limit_key_ttl,
            settings.chat_limit_free_users
        )
        current_limit = settings.chat_limit_free_users
    else:
        current_limit = int(current_limit)

    # Obtém o TTL para informar quando o limite será resetado
    ttl = redis_client.ttl(limit_key)

    return {
        "remaining": current_limit,
        "is_limited": True,
        "reset_time": ttl
    }
