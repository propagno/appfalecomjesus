from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user, get_current_active_user
from app.schemas.gamification import (
    LeaderboardResponse,
    LeaderboardEntryResponse,
    UserRankingResponse
)
from app.services.leaderboard_service import LeaderboardService

router = APIRouter()


@router.get("/", response_model=LeaderboardResponse)
async def get_global_leaderboard(
    skip: int = Query(0, ge=0, description="Quantos itens pular"),
    limit: int = Query(
        10, ge=1, le=100, description="Limite de itens por página"),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    time_period: str = Query(
        "all_time", description="Período de tempo (daily, weekly, monthly, all_time)"),
    current_user: Optional[dict] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna o ranking global de pontos dos usuários.

    Pode ser filtrado por categoria e período de tempo.
    Se o usuário estiver autenticado, inclui sua posição no ranking.
    """
    leaderboard_service = LeaderboardService(db)

    # Obtém o ranking
    leaderboard = await leaderboard_service.get_leaderboard(
        skip=skip,
        limit=limit,
        category=category,
        time_period=time_period
    )

    # Se o usuário estiver autenticado, adiciona sua posição
    if current_user:
        user_ranking = await leaderboard_service.get_user_ranking(
            user_id=current_user["id"],
            category=category,
            time_period=time_period
        )
        leaderboard.user_ranking = user_ranking

    return leaderboard


@router.get("/ranking", response_model=UserRankingResponse)
async def get_user_ranking(
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    time_period: str = Query(
        "all_time", description="Período de tempo (daily, weekly, monthly, all_time)"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna a posição do usuário atual no ranking global.

    Inclui:
    - Posição no ranking
    - Total de pontos
    - Distância para o próximo e anterior no ranking
    """
    leaderboard_service = LeaderboardService(db)
    return await leaderboard_service.get_user_ranking(
        user_id=current_user["id"],
        category=category,
        time_period=time_period
    )


@router.get("/friends", response_model=LeaderboardResponse)
async def get_friends_leaderboard(
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    time_period: str = Query(
        "all_time", description="Período de tempo (daily, weekly, monthly, all_time)"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna o ranking apenas entre amigos do usuário.

    Inclui o usuário atual e seus amigos, ordenados por pontos.
    """
    leaderboard_service = LeaderboardService(db)
    return await leaderboard_service.get_friends_leaderboard(
        user_id=current_user["id"],
        category=category,
        time_period=time_period
    )


@router.get("/categories", response_model=List[str])
async def get_leaderboard_categories(
    current_user: Optional[dict] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna a lista de categorias disponíveis para o ranking.
    """
    leaderboard_service = LeaderboardService(db)
    return await leaderboard_service.get_leaderboard_categories()


@router.get("/periods", response_model=List[str])
async def get_time_periods(
    current_user: Optional[dict] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna a lista de períodos de tempo disponíveis para o ranking.
    """
    return ["daily", "weekly", "monthly", "all_time"]
