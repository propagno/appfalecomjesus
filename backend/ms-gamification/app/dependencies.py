from typing import Generator, Optional, Dict
from fastapi import Depends, HTTPException, status, Cookie
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.models.db import SessionLocal
from app.core.config import settings


def get_db() -> Generator:
    """
    Retorna uma sessão de banco de dados.
    A sessão será fechada após o uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    access_token: Optional[str] = Cookie(None, alias="access_token"),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Dependência para obter o usuário atual a partir do token JWT.
    Retorna o payload do usuário se o token for válido.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not access_token:
        raise credentials_exception

    try:
        payload = jwt.decode(
            access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        # Retornar um dicionário com os dados necessários
        return {
            "id": user_id,
            "sub": user_id,
            "role": payload.get("role", "user")
        }
    except JWTError:
        raise credentials_exception


async def get_current_active_user(current_user: Dict = Depends(get_current_user)) -> Dict:
    """
    Dependência para obter o usuário atual que está ativo.
    Verifica se o usuário está ativo e retorna o payload completo.
    """
    if current_user.get("disabled", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user
