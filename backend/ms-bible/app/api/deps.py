from fastapi import Depends, HTTPException, status, Header
from typing import Optional
import httpx
import os
from jose import jwt, JWTError
import logging

# Configurações de autenticação
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://ms-auth:5000")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

logger = logging.getLogger("ms-bible")


async def get_current_user(authorization: Optional[str] = Header(None)) -> Optional[dict]:
    """
    Extrai e valida o usuário atual a partir do token JWT.
    Este é um middleware opcional, permitindo acesso anônimo se o token não for fornecido.

    Args:
        authorization: O cabeçalho de autorização contendo o token JWT

    Returns:
        O usuário autenticado ou None se não estiver autenticado

    Raises:
        HTTPException: Se o token for inválido
    """
    if not authorization:
        return None

    if not authorization.startswith("Bearer "):
        return None

    token = authorization.replace("Bearer ", "")

    try:
        # Verifica o token localmente para performance
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:
            return None

        return {
            "id": user_id,
            "username": payload.get("username", ""),
            "email": payload.get("email", ""),
            "is_admin": payload.get("is_admin", False)
        }

    except JWTError:
        # Token JWT inválido, mas não vamos barrar o acesso
        return None

    except Exception as e:
        logger.error(f"Erro ao processar token: {str(e)}")
        return None


async def get_current_active_user(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Verifica se o usuário está autenticado e está ativo.
    Este middleware requer autenticação.

    Args:
        current_user: O usuário autenticado pelo get_current_user

    Returns:
        O usuário autenticado

    Raises:
        HTTPException: Se o usuário não estiver autenticado ou não estiver ativo
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Em uma implementação real, verificaríamos se o usuário está ativo
    # no MS-Auth, mas para este exemplo, assumimos que está

    return current_user
