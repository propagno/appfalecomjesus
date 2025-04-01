from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
import logging

from app.core.config import settings
from app.db.session import SessionLocal, get_db
from app.schemas.token import TokenPayload
from app.services.subscription_service import SubscriptionService
from app.services.payment_service import PaymentService
from app.services.ad_reward_service import AdRewardService
from app.services.auth_service import AuthService
from app.services.chat_limit_service import ChatLimitService
from app.services.redis_client import RedisClient

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

logger = logging.getLogger(__name__)

# Singleton do ChatLimitService
_chat_limit_service = None
# Singleton do RedisClient
_redis_client = None


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_redis_client() -> RedisClient:
    """
    Retorna uma instância do cliente Redis.
    Usa um singleton para evitar múltiplas conexões.
    """
    global _redis_client
    if _redis_client is None:
        redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
        if settings.REDIS_PASSWORD:
            redis_url = f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
        _redis_client = RedisClient(redis_url)
    return _redis_client


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> TokenPayload:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return token_data


def get_current_active_user(
    current_user: TokenPayload = Depends(get_current_user),
) -> TokenPayload:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_premium_user(
    current_user: TokenPayload = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> TokenPayload:
    subscription_status = SubscriptionService.get_subscription_status(
        db, current_user.id
    )
    if subscription_status["subscription_status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium subscription required",
        )
    return current_user


def get_subscription_service(db: Session = Depends(get_db)) -> SubscriptionService:
    return SubscriptionService(db)


def get_payment_service(db: Session = Depends(get_db)) -> PaymentService:
    return PaymentService(db)


def get_ad_reward_service(
    db: Session = Depends(get_db),
    redis_client: RedisClient = Depends(get_redis_client)
) -> AdRewardService:
    return AdRewardService(db, redis_client)


def get_chat_limit_service(
    db: Session = Depends(get_db),
    redis_client: RedisClient = Depends(get_redis_client)
) -> ChatLimitService:
    global _chat_limit_service
    if _chat_limit_service is None:
        _chat_limit_service = ChatLimitService(redis_client)
    return _chat_limit_service


async def get_current_user(authorization: Optional[str] = Header(None)) -> Optional[dict]:
    """
    Verifica a autenticação do usuário a partir do cabeçalho Authorization.

    Args:
        authorization: Token de autorização no formato "Bearer <token>"

    Returns:
        Dados do usuário ou None se não autenticado
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None

    token = authorization.replace("Bearer ", "")
    user_data = await AuthService.verify_token(token)

    return user_data


async def get_current_user_id(authorization: Optional[str] = Header(None)) -> str:
    """
    Obtém o ID do usuário atual a partir do token de autorização.

    Args:
        authorization: Token de autorização no formato "Bearer <token>"

    Returns:
        ID do usuário

    Raises:
        HTTPException: Se o usuário não estiver autenticado
    """
    user_data = await get_current_user(authorization)

    if not user_data or "sub" not in user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )

    return user_data["sub"]


def get_user_by_id(user_id: str) -> Optional[dict]:
    """
    Obtém um usuário pelo ID através do MS-Auth.

    Args:
        user_id: ID do usuário a ser buscado

    Returns:
        Dicionário com os dados do usuário ou None se não encontrado
    """
    try:
        return AuthService.get_user_by_id(user_id)
    except Exception as e:
        logger.error(f"Erro ao obter usuário {user_id}: {str(e)}")
        return None
