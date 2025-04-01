import logging
from typing import AsyncGenerator, Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.user import User
from app.services.ads_service import AdsService
from app.services.cache_service import CacheService
from app.services.certificate_service import CertificateService
from app.services.chat_service import ChatService
from app.services.gamification_service import GamificationService
from app.services.hotmart_service import HotmartService
from app.services.monetization_service import MonetizationService
from app.services.openai_service import OpenAIService
from app.services.reflection_service import ReflectionService
from app.services.stripe_service import StripeService

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_db() -> Generator:
    """
    Retorna sessão do banco de dados.

    Yields:
        Sessão do SQLAlchemy

    Raises:
        Exception: Se erro na conexão
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Retorna usuário autenticado.

    Args:
        token: Token JWT
        db: Sessão do banco

    Returns:
        Usuário autenticado

    Raises:
        HTTPException: Se token inválido
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token de acesso inválido",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        # Decodifica token
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception

        # Busca usuário
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise credentials_exception

        return user

    except JWTError:
        raise credentials_exception


async def get_premium_user(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """
    Retorna usuário premium.

    Args:
        user: Usuário atual
        db: Sessão do banco

    Returns:
        Usuário premium

    Raises:
        HTTPException: Se não é premium
    """
    if not user.is_premium:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Recurso disponível apenas para usuários premium"
        )
    return user


async def get_admin_user(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """
    Retorna usuário admin.

    Args:
        user: Usuário atual
        db: Sessão do banco

    Returns:
        Usuário admin

    Raises:
        HTTPException: Se não é admin
    """
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Recurso disponível apenas para administradores"
        )
    return user


def get_ads_service(
    db: Session = Depends(get_db)
) -> AdsService:
    """
    Retorna serviço de anúncios.

    Args:
        db: Sessão do banco

    Returns:
        Instância do AdsService
    """
    return AdsService(db)


def get_cache_service() -> CacheService:
    """
    Retorna serviço de cache.

    Returns:
        Instância do CacheService
    """
    return CacheService()


def get_certificate_service(
    db: Session = Depends(get_db)
) -> CertificateService:
    """
    Retorna serviço de certificados.

    Args:
        db: Sessão do banco

    Returns:
        Instância do CertificateService
    """
    return CertificateService(db)


def get_chat_service(
    db: Session = Depends(get_db)
) -> ChatService:
    """
    Retorna serviço de chat.

    Args:
        db: Sessão do banco

    Returns:
        Instância do ChatService
    """
    return ChatService(db)


def get_gamification_service(
    db: Session = Depends(get_db)
) -> GamificationService:
    """
    Retorna serviço de gamificação.

    Args:
        db: Sessão do banco

    Returns:
        Instância do GamificationService
    """
    return GamificationService(db)


def get_hotmart_service(
    db: Session = Depends(get_db)
) -> HotmartService:
    """
    Retorna serviço do Hotmart.

    Args:
        db: Sessão do banco

    Returns:
        Instância do HotmartService
    """
    return HotmartService(db)


def get_monetization_service(
    db: Session = Depends(get_db)
) -> MonetizationService:
    """
    Retorna serviço de monetização.

    Args:
        db: Sessão do banco

    Returns:
        Instância do MonetizationService
    """
    return MonetizationService(db)


def get_openai_service() -> OpenAIService:
    """
    Retorna serviço da OpenAI.

    Returns:
        Instância do OpenAIService
    """
    return OpenAIService()


def get_reflection_service(
    db: Session = Depends(get_db)
) -> ReflectionService:
    """
    Retorna serviço de reflexões.

    Args:
        db: Sessão do banco

    Returns:
        Instância do ReflectionService
    """
    return ReflectionService(db)


def get_stripe_service(
    db: Session = Depends(get_db)
) -> StripeService:
    """
    Retorna serviço do Stripe.

    Args:
        db: Sessão do banco

    Returns:
        Instância do StripeService
    """
    return StripeService(db)
