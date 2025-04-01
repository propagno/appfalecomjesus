from fastapi import Depends, HTTPException, status, Security, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
import jwt
from datetime import datetime, timedelta
import uuid

from app.core.config import get_settings, Settings

# JWT Bearer Security Scheme
security = HTTPBearer(auto_error=False)


async def get_token_from_cookie(
    access_token: Optional[str] = Cookie(None, alias="access_token")
) -> Optional[str]:
    """
    Extrai o token JWT do cookie HTTP-Only.
    """
    return access_token


async def get_token_from_header(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security)
) -> Optional[str]:
    """
    Extrai o token JWT do cabeçalho de autorização.
    """
    return credentials.credentials if credentials else None


async def validate_token(
    token: Optional[str] = Depends(get_token_from_cookie),
    header_token: Optional[str] = Depends(get_token_from_header),
    settings: Settings = Depends(get_settings)
) -> Dict[str, Any]:
    """
    Valida o token JWT e retorna o payload se válido.

    Prioridade: 1) Token do Cookie, 2) Token do Cabeçalho

    Raises:
        HTTPException: Se o token for inválido ou expirado
    """
    # Usar o token do cookie ou do cabeçalho (prioridade para o cookie)
    token_to_validate = token or header_token

    if not token_to_validate:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autorizado: Token não fornecido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            token_to_validate,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        # Verificar se o token expirou
        expiration = datetime.fromtimestamp(payload.get("exp", 0))
        if datetime.utcnow() > expiration:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não autorizado: Token expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autorizado: Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_id(
    payload: Dict[str, Any] = Depends(validate_token)
) -> uuid.UUID:
    """
    Extrai o ID do usuário do payload do token JWT.

    Raises:
        HTTPException: Se o sub não estiver presente no payload
    """
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autorizado: Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        return uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autorizado: ID de usuário inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
