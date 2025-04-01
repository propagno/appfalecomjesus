from typing import Annotated, Generator, Optional
from fastapi import Depends, HTTPException, status, Cookie, Request, Header
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError, BaseModel
from sqlalchemy.orm import Session
import logging
from datetime import datetime
import jwt
from jwt.exceptions import PyJWTError
import httpx

from app.core.config import get_settings
from app.infrastructure.database import get_db
from app.domain.study.service import StudyService

# Import these from ms-auth when implementing the authentication middleware
# from app.schemas.auth import TokenPayload, User

settings = get_settings()
logger = logging.getLogger("api")

# Definir um esquema OAuth que não levanta erro quando não tem token


class OptionalOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        try:
            return await super().__call__(request)
        except HTTPException:
            return None


# Usar o esquema OAuth2 opcional
oauth2_scheme = OptionalOAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/token",
    auto_error=False
)

# Criar modelo para decodificação do token


class TokenPayload(BaseModel):
    sub: str
    exp: datetime


def get_study_service(db: Session = Depends(get_db)) -> StudyService:
    """
    Get an instance of the StudyService.
    """
    return StudyService(db)


async def get_current_user(authorization: str = Header(None)) -> Optional[dict]:
    """
    Validate JWT token and return user info.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação não fornecido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Check if the token starts with "Bearer "
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de autenticação inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify token with auth service
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(
                    f"{settings.MS_AUTH_URL}/api/v1/auth/verify-token",
                    json={"token": token}
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Token inválido ou expirado",
                        headers={"WWW-Authenticate": "Bearer"},
                    )

                user_data = response.json()
                return user_data
        except httpx.RequestError as e:
            logger.error(f"Error calling auth service: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Erro ao verificar token de autenticação",
            )

    except PyJWTError as e:
        logger.error(f"JWT verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro de autenticação",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Verify that the user is active.
    """
    if not current_user.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo",
        )
    return current_user


def verify_service_api_key(authorization: str = Header(None)) -> None:
    """
    Verify that the request has a valid service API key.
    Used for service-to-service communication.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key não fornecida",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Check if the token starts with "Bearer "
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Formato de API key inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify the API key
        if token != settings.SERVICE_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key inválida",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return None
    except Exception as e:
        logger.error(f"API key verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro na verificação da API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
