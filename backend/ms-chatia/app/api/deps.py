from typing import Annotated, Dict, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import decode_token_from_header
from app.core.database import get_session


def get_current_user(authorization: Optional[str] = None) -> Dict:
    """
    Função de dependência para obter o usuário autenticado a partir do token JWT.

    Args:
        authorization: Token de autenticação no formato 'Bearer {token}'

    Returns:
        Dict: Dados do usuário autenticado

    Raises:
        HTTPException: Se o token for inválido ou estiver expirado
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação não fornecido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_data = decode_token_from_header(authorization)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Erro de autenticação: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_db() -> Session:
    """
    Função de dependência para obter uma sessão do banco de dados.

    Returns:
        Session: Sessão do SQLAlchemy para interação com o banco
    """
    db = get_session()
    try:
        yield db
    finally:
        db.close()
