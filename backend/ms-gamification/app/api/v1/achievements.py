from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from typing import List, Optional
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user, get_current_active_user
from app.schemas.gamification import (
    AchievementResponse,
    AchievementListResponse,
    UserAchievementResponse,
    AchievementDetail
)
from app.services.achievement_service import AchievementService

router = APIRouter()


@router.get("/", response_model=AchievementListResponse)
async def get_achievements(
    skip: int = Query(0, ge=0, description="Quantos itens pular"),
    limit: int = Query(
        10, ge=1, le=100, description="Limite de itens por página"),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    difficulty: Optional[str] = Query(
        None, description="Filtrar por dificuldade"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista todas as conquistas disponíveis no sistema.

    Pode ser filtrado por categoria e dificuldade e paginado.
    """
    achievement_service = AchievementService(db)
    return await achievement_service.get_achievements(
        skip=skip,
        limit=limit,
        category=category,
        difficulty=difficulty
    )


@router.get("/user", response_model=UserAchievementResponse)
async def get_user_achievements(
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna as conquistas do usuário atual, incluindo:
    - Conquistas já obtidas
    - Progresso em conquistas pendentes
    - Últimas conquistas desbloqueadas
    """
    achievement_service = AchievementService(db)
    return await achievement_service.get_user_achievements(current_user["id"])


@router.get("/{achievement_id}", response_model=AchievementResponse)
async def get_achievement_detail(
    achievement_id: str = Path(..., description="ID da conquista"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna detalhes de uma conquista específica.

    Se o usuário estiver autenticado, inclui informações de progresso.
    """
    achievement_service = AchievementService(db)

    # Obter detalhes da conquista
    achievement = await achievement_service.get_achievement_by_id(achievement_id)

    # Se o usuário estiver autenticado, adiciona dados de progresso
    if current_user:
        user_progress = await achievement_service.get_user_achievement_progress(
            user_id=current_user["id"],
            achievement_id=achievement_id
        )
        achievement.user_progress = user_progress

    return achievement


@router.get("/categories", response_model=List[str])
async def get_achievement_categories(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna a lista de categorias de conquistas disponíveis.
    """
    achievement_service = AchievementService(db)
    return await achievement_service.get_achievement_categories()


@router.post("/{achievement_id}/check", response_model=AchievementResponse)
async def check_achievement(
    achievement_id: str = Path(..., description="ID da conquista a verificar"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Verifica se o usuário completou os requisitos para uma conquista específica.

    Se os requisitos forem atendidos, a conquista é marcada como concluída.
    Retorna o estado atualizado da conquista.
    """
    achievement_service = AchievementService(db)
    return await achievement_service.check_achievement(
        user_id=current_user["id"],
        achievement_id=achievement_id
    )


@router.get("/user/{user_id}", response_model=UserAchievementResponse)
async def get_other_user_achievements(
    user_id: str = Path(..., description="ID do usuário"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna as conquistas de outro usuário.

    Somente administradores podem ver as conquistas de outros usuários.
    """
    # Verificar se o usuário atual é administrador
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Somente administradores podem ver conquistas de outros usuários"
        )

    achievement_service = AchievementService(db)
    return await achievement_service.get_user_achievements(user_id)
