from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.db.session import get_async_session
from app.core.config import settings
from app.core.security import ALGORITHM, decode_jwt
from app.schemas.user import UserInDB
from app.services.redis_client import RedisClient
from app.repositories import (
    SubscriptionRepository,
    AdRewardRepository,
    SubscriptionPlanRepository,
    PaymentTransactionRepository
)
from app.services import (
    SubscriptionService,
    AdRewardService,
    PaymentService
)

# Configurar logger
logger = logging.getLogger(__name__)

# Instância global do RedisClient
redis_client = RedisClient(settings.REDIS_URL)

# Security
security = HTTPBearer()


async def get_db() -> Generator[AsyncSession, None, None]:
    """
    Dependência para obter uma sessão de banco de dados.
    """
    async for session in get_async_session():
        yield session


async def get_redis_client() -> RedisClient:
    """
    Dependência para obter o cliente Redis.
    """
    return redis_client


# Dependência para autenticação via JWT
async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> UserInDB:
    """
    Verifica o token JWT e retorna o usuário atualmente autenticado.

    Args:
        request: Request - O objeto de requisição.
        credentials: HTTPAuthorizationCredentials - As credenciais de autenticação.
        db: AsyncSession - A sessão do banco de dados.

    Returns:
        UserInDB - O usuário autenticado.

    Raises:
        HTTPException: Se o token for inválido ou expirado.
    """
    try:
        token = credentials.credentials
        payload = decode_jwt(token)
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Extrair informações do usuário do payload
        user = UserInDB(
            id=user_id,
            email=payload.get("email", ""),
            is_active=payload.get("is_active", True),
            is_admin=payload.get("is_admin", False)
        )

        return user
    except jwt.PyJWTError as e:
        logger.error(f"Erro ao verificar JWT: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Erro ao processar autenticação: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor na autenticação",
        )


# Repositories
async def get_subscription_repository(db: AsyncSession = Depends(get_db)) -> SubscriptionRepository:
    """Retorna um repositório de assinaturas."""
    return SubscriptionRepository(db)


async def get_ad_reward_repository(db: AsyncSession = Depends(get_db)) -> AdRewardRepository:
    """Retorna um repositório de recompensas por anúncios."""
    return AdRewardRepository(db)


async def get_subscription_plan_repository(db: AsyncSession = Depends(get_db)) -> SubscriptionPlanRepository:
    """Retorna um repositório de planos de assinatura."""
    return SubscriptionPlanRepository(db)


async def get_payment_transaction_repository(db: AsyncSession = Depends(get_db)) -> PaymentTransactionRepository:
    """Retorna um repositório de transações de pagamento."""
    return PaymentTransactionRepository(db)


# Services
async def get_subscription_service(
    subscription_repo: SubscriptionRepository = Depends(
        get_subscription_repository),
    plan_repo: SubscriptionPlanRepository = Depends(
        get_subscription_plan_repository),
    redis: RedisClient = Depends(get_redis_client)
) -> SubscriptionService:
    """Retorna um serviço de assinaturas."""
    return SubscriptionService(subscription_repo, plan_repo, redis)


async def get_ad_reward_service(
    reward_repo: AdRewardRepository = Depends(get_ad_reward_repository),
    redis: RedisClient = Depends(get_redis_client)
) -> AdRewardService:
    """Retorna um serviço de recompensas por anúncios."""
    return AdRewardService(reward_repo, redis)


async def get_payment_service(
    transaction_repo: PaymentTransactionRepository = Depends(
        get_payment_transaction_repository),
    subscription_service: SubscriptionService = Depends(
        get_subscription_service)
) -> PaymentService:
    """Retorna um serviço de pagamentos."""
    return PaymentService(transaction_repo, subscription_service)
