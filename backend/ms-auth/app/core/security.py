from datetime import datetime, timedelta
from typing import Any, Optional, Union, Dict
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..domain.models import User
from ..infrastructure.database import get_db
from .config import get_settings
from app.domain.auth.models import UserSubscription, SubscriptionType, SubscriptionStatus

settings = get_settings()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 password bearer token scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT refresh token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=7))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Dependency to get the current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key,
                             algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


def validate_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Validate and decode a JWT token.
    """
    try:
        payload = jwt.decode(token, settings.secret_key,
                             algorithms=[settings.algorithm])
        return payload
    except jwt.JWTError:
        return None


def check_premium_subscription(user_id: str, db: Session) -> bool:
    """
    Verifica se o usuário possui uma assinatura premium ativa.

    Args:
        user_id: ID do usuário
        db: Sessão do banco de dados

    Returns:
        True se o usuário possui assinatura premium ativa, False caso contrário
    """
    subscription = db.query(UserSubscription).filter(
        UserSubscription.user_id == user_id
    ).first()

    if not subscription:
        return False

    # Verificar se é uma assinatura premium ativa
    is_premium = subscription.subscription_type == SubscriptionType.PREMIUM
    is_active = subscription.status == SubscriptionStatus.ACTIVE

    # Verificar se não expirou (se tiver data de expiração)
    not_expired = True
    if subscription.expiration_date:
        not_expired = subscription.expiration_date > datetime.utcnow()

    return is_premium and is_active and not_expired


def get_premium_status(user_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Obtém o status completo da assinatura premium do usuário.

    Args:
        user_id: ID do usuário
        db: Sessão do banco de dados

    Returns:
        Dicionário com informações sobre a assinatura premium
    """
    subscription = db.query(UserSubscription).filter(
        UserSubscription.user_id == user_id
    ).first()

    if not subscription:
        return {
            "is_premium": False,
            "active": False,
            "subscription_type": "free",
            "days_remaining": 0
        }

    # Verificar status
    is_premium = subscription.subscription_type == SubscriptionType.PREMIUM
    is_active = subscription.status == SubscriptionStatus.ACTIVE

    # Calcular dias restantes
    days_remaining = 0
    if subscription.expiration_date:
        delta = subscription.expiration_date - datetime.utcnow()
        days_remaining = max(0, delta.days)

        # Se a assinatura premium expirou, não é mais premium
        if days_remaining == 0 and subscription.expiration_date < datetime.utcnow():
            is_premium = False

    return {
        "is_premium": is_premium and is_active,
        "active": is_active,
        "subscription_type": subscription.subscription_type.value,
        "status": subscription.status.value,
        "days_remaining": days_remaining,
        "expiration_date": subscription.expiration_date,
        "payment_gateway": subscription.payment_gateway
    }
