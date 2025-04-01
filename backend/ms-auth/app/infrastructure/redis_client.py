import redis
from ..core.config import get_settings

settings = get_settings()

# Create Redis connection
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

# Check Redis connection


def check_redis_connection():
    try:
        return redis_client.ping()
    except redis.ConnectionError:
        return False
