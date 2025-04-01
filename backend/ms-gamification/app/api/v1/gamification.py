from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from ...dependencies import get_db, get_current_user
from ...services import GamificationService
from ...schemas import (
    UserPoint,
    AddPointsRequest,
    AddPointsResponse,
    AchievementResponse,
    CheckAchievementsResponse
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Endpoint de verificação de saúde do serviço"""
    return {"status": "ok", "service": "ms-gamification"}


@router.get("/points", response_model=UserPoint)
async def get_points(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter pontos do usuário atual"""
    try:
        user_id = current_user.get("sub")
        gamification_service = GamificationService(db)
        return gamification_service.get_user_points(user_id)
    except Exception as e:
        logger.error(
            f"Erro ao obter pontos do usuário {current_user.get('sub')}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter pontos do usuário"
        )


@router.post("/add-points", response_model=AddPointsResponse)
async def add_points(
    request: AddPointsRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Adicionar pontos ao usuário atual"""
    try:
        user_id = current_user.get("sub")
        gamification_service = GamificationService(db)
        return gamification_service.add_points(user_id, request.amount, request.reason)
    except HTTPException as he:
        # Repassar exceções HTTP já formatadas
        raise he
    except Exception as e:
        logger.error(
            f"Erro ao adicionar pontos para usuário {current_user.get('sub')}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao adicionar pontos"
        )


@router.get("/achievements", response_model=List[AchievementResponse])
async def get_achievements(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter todas as conquistas do usuário atual"""
    try:
        user_id = current_user.get("sub")
        gamification_service = GamificationService(db)
        return gamification_service.get_user_achievements(user_id)
    except Exception as e:
        logger.error(
            f"Erro ao obter conquistas do usuário {current_user.get('sub')}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter conquistas do usuário"
        )


@router.get("/check-achievements", response_model=CheckAchievementsResponse)
async def check_achievements(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Verificar se há novas conquistas disponíveis para o usuário atual"""
    try:
        user_id = current_user.get("sub")
        gamification_service = GamificationService(db)
        new_achievements = gamification_service.check_new_achievements(user_id)

        total_achievements = len(
            gamification_service.get_user_achievements(user_id))

        return CheckAchievementsResponse(
            new_achievements=new_achievements,
            total_achievements=total_achievements
        )
    except Exception as e:
        logger.error(
            f"Erro ao verificar conquistas para usuário {current_user.get('sub')}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao verificar conquistas"
        )


@router.get("/notifications", response_model=List[AchievementResponse])
async def get_notifications(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter notificações de novas conquistas"""
    try:
        user_id = current_user.get("sub")
        gamification_service = GamificationService(db)
        return gamification_service.get_new_notifications(user_id)
    except Exception as e:
        logger.error(
            f"Erro ao obter notificações para usuário {current_user.get('sub')}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter notificações"
        )


@router.post("/unlock-by-condition/{condition_type}", response_model=List[AchievementResponse])
async def unlock_by_condition(
    condition_type: str,
    value: int = 1,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Desbloquear conquistas por condição específica
    Condition types: study_completed, chat_used, reflection_saved, days_streak
    """
    valid_conditions = ['study_completed',
                        'chat_used', 'reflection_saved', 'days_streak']
    if condition_type not in valid_conditions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de condição inválido. Opções: {', '.join(valid_conditions)}"
        )

    try:
        user_id = current_user.get("sub")
        gamification_service = GamificationService(db)
        return gamification_service.unlock_achievement_by_condition(user_id, condition_type, value)
    except Exception as e:
        logger.error(
            f"Erro ao desbloquear conquistas por condição para usuário {current_user.get('sub')}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao desbloquear conquistas"
        )
