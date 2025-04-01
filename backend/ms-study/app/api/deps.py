from typing import Generator, Optional, Dict, Any
from fastapi import Depends, HTTPException, status, Request, Header
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
import logging

from app.db.session import get_db
from app.core.config import get_settings
from app.repositories.study_plan_repository import StudyPlanRepository
from app.repositories.study_section_repository import StudySectionRepository
from app.repositories.study_content_repository import StudyContentRepository
from app.repositories.user_study_progress_repository import UserStudyProgressRepository
from app.repositories.certificate_repository import CertificateRepository
from app.services.study_plan_service import StudyPlanService
from app.services.study_progress_service import StudyProgressService
from app.services.certificate_service import CertificateService
from app.services.user_service import UserService

# Obtendo configurações
settings = get_settings()

# Configuração do logger
logger = logging.getLogger(__name__)

# Configuração do serviço de autenticação
AUTH_SERVICE_URL = settings.AUTH_SERVICE_URL
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{AUTH_SERVICE_URL}/api/auth/login", auto_error=False)


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[Dict[str, Any]]:
    """
    Dependência para verificar o token JWT e obter o usuário atual.
    Permite acesso anônimo se não houver token.

    Args:
        authorization: Token de autorização no formato "Bearer {token}"
        db: Sessão do banco de dados

    Returns:
        Dados do usuário ou None se não houver token

    Raises:
        HTTPException: Quando o token é inválido
    """
    if not authorization:
        return None

    try:
        # Extrair o token do cabeçalho
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None

        # Decodificar o token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            return None

        # Retornar dados básicos do usuário extraídos do token
        return {
            "id": user_id,
            "email": payload.get("email"),
            "is_active": payload.get("is_active", True),
            "is_premium": payload.get("is_premium", False),
            "role": payload.get("role", "user")
        }
    except (JWTError, ValidationError, ValueError) as e:
        logger.warning(f"Token inválido: {str(e)}")
        return None


async def get_current_active_user(
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Dependência para obter um usuário autenticado e ativo.

    Args:
        current_user: Dados do usuário obtidos do token

    Returns:
        Dados do usuário autenticado

    Raises:
        HTTPException: Quando o usuário não está autenticado ou está inativo
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticação necessária",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar se o usuário está ativo (apenas como exemplo)
    # Em uma implementação real, você pode verificar o status com o MS-Auth

    return current_user

# Repositórios


def get_study_plan_repository(db: Session = Depends(get_db)) -> StudyPlanRepository:
    return StudyPlanRepository(db)


def get_study_section_repository(db: Session = Depends(get_db)) -> StudySectionRepository:
    return StudySectionRepository(db)


def get_study_content_repository(db: Session = Depends(get_db)) -> StudyContentRepository:
    return StudyContentRepository(db)


def get_user_study_progress_repository(db: Session = Depends(get_db)) -> UserStudyProgressRepository:
    return UserStudyProgressRepository(db)


def get_certificate_repository(db: Session = Depends(get_db)) -> CertificateRepository:
    return CertificateRepository(db)


# Serviços
def get_user_service() -> UserService:
    """
    Retorna uma instância de UserService.
    """
    return UserService()


def get_study_plan_service(
    study_plan_repository: StudyPlanRepository = Depends(
        get_study_plan_repository),
    study_section_repository: StudySectionRepository = Depends(
        get_study_section_repository),
    study_content_repository: StudyContentRepository = Depends(
        get_study_content_repository)
) -> StudyPlanService:
    """
    Retorna uma instância de StudyPlanService.
    """
    return StudyPlanService(
        study_plan_repository,
        study_section_repository,
        study_content_repository
    )


def get_study_progress_service(
    user_study_progress_repository: UserStudyProgressRepository = Depends(
        get_user_study_progress_repository),
    study_plan_repository: StudyPlanRepository = Depends(
        get_study_plan_repository),
    study_section_repository: StudySectionRepository = Depends(
        get_study_section_repository)
) -> StudyProgressService:
    """
    Retorna uma instância de StudyProgressService.
    """
    return StudyProgressService(
        user_study_progress_repository,
        study_plan_repository,
        study_section_repository
    )


def get_certificate_service(
    certificate_repository: CertificateRepository = Depends(
        get_certificate_repository),
    study_plan_repository: StudyPlanRepository = Depends(
        get_study_plan_repository),
    user_study_progress_repository: UserStudyProgressRepository = Depends(
        get_user_study_progress_repository),
    user_service: UserService = Depends(get_user_service)
) -> CertificateService:
    """
    Retorna uma instância de CertificateService.
    """
    return CertificateService(
        certificate_repository,
        study_plan_repository,
        user_study_progress_repository,
        user_service
    )
