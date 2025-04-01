import logging
import jwt
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any

from app.core.config import settings
from app.db.session import get_db
from app.services.points_service import PointsService
from app.services.achievement_service import AchievementService
from app.services.leaderboard_service import LeaderboardService

# Configuração de logging
logger = logging.getLogger(__name__)

security = HTTPBearer()


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[Dict[str, Any]]:
    """
    Valida o token JWT e retorna dados do usuário atual.

    Args:
        authorization: Token JWT no header Authorization
        db: Sessão do banco de dados

    Returns:
        Dicionário com dados do usuário ou None

    Raises:
        HTTPException: Se o token for inválido
    """
    # Se não houver token, permite acesso anônimo para alguns endpoints
    if not authorization:
        return None

    try:
        # Remove o prefixo "Bearer " se existir
        if authorization.startswith("Bearer "):
            token = authorization.replace("Bearer ", "")
        else:
            token = authorization

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # Extrair dados do usuário do payload
        user_id = payload.get("sub")
        if not user_id:
            return None

        # Retorna dados básicos do usuário
        return {
            "user_id": user_id,
            "email": payload.get("email"),
            "role": payload.get("role", "user")
        }
    except jwt.ExpiredSignatureError:
        logger.warning("Token JWT expirado")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação expirado"
        )
    except jwt.JWTError as e:
        logger.warning(f"Erro na validação do token JWT: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação inválido"
        )
    except Exception as e:
        logger.error(f"Erro ao validar token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro de autenticação"
        )


async def get_current_active_user(
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Verifica se o usuário está autenticado e ativo.

    Args:
        current_user: Dados do usuário atual

    Returns:
        Dados do usuário

    Raises:
        HTTPException: Se o usuário não estiver autenticado
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado"
        )

    # Neste exemplo simplificado, assumimos que o usuário está sempre ativo
    # Em uma implementação real, verificaríamos com o serviço de autenticação

    return current_user


def get_points_service(db: Session = Depends(get_db)) -> PointsService:
    """
    Cria e retorna uma instância do serviço de pontos.

    Args:
        db: Sessão do banco de dados

    Returns:
        Instância do PointsService
    """
    return PointsService(db)


def get_achievement_service(db: Session = Depends(get_db)) -> AchievementService:
    """
    Cria e retorna uma instância do serviço de conquistas.

    Args:
        db: Sessão do banco de dados

    Returns:
        Instância do AchievementService
    """
    return AchievementService(db)


def get_leaderboard_service(db: Session = Depends(get_db)) -> LeaderboardService:
    """
    Cria e retorna uma instância do serviço de leaderboard.

    Args:
        db: Sessão do banco de dados

    Returns:
        Instância do LeaderboardService
    """
    return LeaderboardService(db)


def check_admin_role(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
) -> Dict[str, Any]:
    """
    Verifica se o usuário tem permissão de administrador.

    Args:
        current_user: Dados do usuário atual

    Returns:
        Dados do usuário

    Raises:
        HTTPException: Se o usuário não tiver permissão de administrador
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operação restrita a administradores"
        )

    return current_user
