import redis
from app.core.config import settings

# Criar cliente Redis
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

# Função para verificar conexão


def check_redis_connection():
    try:
        redis_client.ping()
        return True
    except redis.ConnectionError:
        return False
