from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.orm import Session
from typing import Optional
from jose import JWTError, jwt
import json

from app.domain.auth.service import AuthService
from app.infrastructure.database import get_db
from app.core.config import get_settings
from app.core.security import check_premium_subscription

settings = get_settings()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


def get_current_user_id(
    access_token: Optional[str] = Cookie(None, alias="access_token")
) -> str:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(
            access_token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def check_premium_access(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> str:
    """
    Verifica se o usuário tem acesso premium e lança uma exceção se não tiver.

    Args:
        user_id: ID do usuário
        db: Sessão do banco de dados

    Returns:
        ID do usuário se tiver acesso premium

    Raises:
        HTTPException: Se o usuário não tiver acesso premium
    """
    if not check_premium_subscription(user_id, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium subscription required for this feature"
        )

    return user_id


def get_admin_user(
    user_id: str = Depends(get_current_user_id),
    auth_service: AuthService = Depends(get_auth_service)
) -> str:
    """
    Verifica se o usuário é administrador e lança uma exceção se não for.

    Args:
        user_id: ID do usuário
        auth_service: Serviço de autenticação

    Returns:
        ID do usuário se for administrador

    Raises:
        HTTPException: Se o usuário não for administrador
    """
    user = auth_service.get_user_by_id(user_id)
    if not user or not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return user_id
