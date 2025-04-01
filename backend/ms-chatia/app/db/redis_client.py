import redis
from app.core.config import settings

# Criar cliente Redis a partir da URL de configuração
redis_client = redis.from_url(settings.REDIS_URL)


def get_chat_limit_key(user_id: str) -> str:
    """
    Gera a chave para o limite de chat de um usuário específico

    Args:
        user_id: ID do usuário

    Returns:
        Chave formatada para o Redis
    """
    return f"chat_limit:{user_id}"


def get_remaining_messages(user_id: str) -> int:
    """
    Obtém o número de mensagens restantes para um usuário no dia

    Args:
        user_id: ID do usuário

    Returns:
        Número de mensagens restantes ou o limite total se não existir
    """
    key = get_chat_limit_key(user_id)
    remaining = redis_client.get(key)

    if remaining is None:
        # Se não existe, retorna o limite completo
        return settings.CHAT_LIMIT_FREE_USERS

    return int(remaining)


def decrement_remaining_messages(user_id: str) -> int:
    """
    Decrementa o contador de mensagens restantes para um usuário

    Args:
        user_id: ID do usuário

    Returns:
        Número atualizado de mensagens restantes
    """
    key = get_chat_limit_key(user_id)
    remaining = redis_client.get(key)

    if remaining is None:
        # Inicializa com o limite total menos 1
        new_value = settings.CHAT_LIMIT_FREE_USERS - 1
        redis_client.set(key, new_value, ex=settings.CHAT_LIMIT_KEY_TTL)
        return new_value

    # Decrementa o valor existente
    new_value = redis_client.decr(key)
    return int(new_value)


def increment_remaining_messages(user_id: str, amount: int = 5) -> int:
    """
    Incrementa o contador de mensagens restantes (usado após assistir anúncio)

    Args:
        user_id: ID do usuário
        amount: Quantidade de mensagens a adicionar

    Returns:
        Número atualizado de mensagens restantes
    """
    key = get_chat_limit_key(user_id)
    remaining = redis_client.get(key)

    if remaining is None:
        # Inicializa com o limite total + quantidade
        new_value = settings.CHAT_LIMIT_FREE_USERS + amount
        redis_client.set(key, new_value, ex=settings.CHAT_LIMIT_KEY_TTL)
        return new_value

    # Incrementa o valor existente
    new_value = redis_client.incrby(key, amount)
    return int(new_value)


def reset_chat_limit(user_id: str) -> int:
    """
    Reinicia o contador de mensagens para o limite máximo

    Args:
        user_id: ID do usuário

    Returns:
        Novo limite (valor máximo)
    """
    key = get_chat_limit_key(user_id)
    redis_client.set(key, settings.CHAT_LIMIT_FREE_USERS,
                     ex=settings.CHAT_LIMIT_KEY_TTL)
    return settings.CHAT_LIMIT_FREE_USERS
