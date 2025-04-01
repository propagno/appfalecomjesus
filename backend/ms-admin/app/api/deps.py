from ..schemas.auth import TokenPayload, User
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from typing import Generator, Optional
import httpx
import os
from datetime import datetime

# Configurações de autenticação
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://ms-auth:5000")

# Modelo para informações do token


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Valida o token JWT e retorna o usuário atual.
    Esta função faz uma chamada ao serviço de autenticação para verificar o token.
    """
    try:
        # Chamar o serviço de autenticação para validar o token
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/api/auth/validate-token",
                headers={"Authorization": f"Bearer {token}"}
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido ou expirado",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            user_data = response.json()
            return User(**user_data)

    except (JWTError, ValidationError, httpx.RequestError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Verifica se o usuário atual tem privilégios de administrador.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O usuário não possui privilégios de administrador",
        )
    return current_user


def get_db() -> Generator:
    """
    Fornece uma sessão do banco de dados para as operações de API.
    """
    from ..db.session import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
