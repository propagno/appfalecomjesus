from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool
from app.core.config import settings
from typing import Optional
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

# Pools de conexão para diferentes bancos
_redis_pools: dict[int, ConnectionPool] = {}


def parse_redis_url(url: str) -> dict:
    """
    Parse a Redis URL into connection parameters.
    """
    parsed = urlparse(url)
    return {
        'host': parsed.hostname or 'localhost',
        'port': parsed.port or 6379,
        'password': parsed.password,
        'username': parsed.username
    }


def get_redis_pool(db: int = 0) -> ConnectionPool:
    """
    Retorna um pool de conexões Redis para o banco especificado.
    Reutiliza pools existentes para evitar criar conexões desnecessárias.
    """
    if db not in _redis_pools:
        try:
            redis_params = parse_redis_url(settings.REDIS_URL)
            _redis_pools[db] = ConnectionPool(
                **redis_params,
                db=db,
                decode_responses=True,
                max_connections=10,
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True
            )
        except Exception as e:
            logger.error(
                f"Erro ao criar pool de conexões Redis para db {db}: {e}")
            raise
    return _redis_pools[db]


async def get_redis_client(db: int = 0) -> Redis:
    """
    Retorna um cliente Redis assíncrono configurado para o banco especificado.
    """
    try:
        pool = get_redis_pool(db)
        return Redis(connection_pool=pool)
    except Exception as e:
        logger.error(f"Erro ao criar cliente Redis: {e}")
        raise


async def check_redis_connection() -> bool:
    """
    Verifica se a conexão com o Redis está funcionando.
    """
    try:
        redis = await get_redis_client()
        await redis.ping()
        return True
    except Exception as e:
        logger.error(f"Erro ao conectar com Redis: {e}")
        return False


async def clear_redis_db(db: int) -> None:
    """
    Limpa todos os dados de um banco Redis específico.
    Útil para testes e limpeza de cache.
    """
    try:
        redis = await get_redis_client(db)
        await redis.flushdb()
    except Exception as e:
        logger.error(f"Erro ao limpar banco Redis {db}: {e}")
        raise


async def close_redis_connections() -> None:
    """
    Fecha todas as conexões Redis.
    Deve ser chamado ao encerrar a aplicação.
    """
    for pool in _redis_pools.values():
        await pool.disconnect()
