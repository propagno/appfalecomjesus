from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status
from typing import List, Optional
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user, get_current_active_user
from app.schemas.gamification import (
    UserPointsResponse,
    PointsHistoryResponse,
    PointsAddRequest,
    PointsSubtractRequest,
    UserPointsDetail
)
from app.services.points_service import PointsService

router = APIRouter()


@router.get("/", response_model=UserPointsResponse)
async def get_user_points(
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna os pontos do usuário atual, incluindo total e detalhes por categoria.
    """
    points_service = PointsService(db)
    return await points_service.get_user_points(current_user["id"])


@router.get("/history", response_model=PointsHistoryResponse)
async def get_points_history(
    skip: int = Query(0, ge=0, description="Quantos itens pular"),
    limit: int = Query(
        10, ge=1, le=100, description="Limite de itens por página"),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna o histórico de transações de pontos do usuário.

    Pode ser filtrado por categoria e paginado.
    """
    points_service = PointsService(db)
    return await points_service.get_points_history(
        user_id=current_user["id"],
        skip=skip,
        limit=limit,
        category=category
    )


@router.post("/add", response_model=UserPointsDetail, status_code=status.HTTP_200_OK)
async def add_points(
    points_data: PointsAddRequest,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Adiciona pontos ao usuário atual.

    Requer:
    - Quantidade de pontos
    - Categoria (oração, estudo, compartilhamento, etc)
    - Descrição da ação realizada

    Somente ações autorizadas pelo sistema podem adicionar pontos.
    """
    points_service = PointsService(db)
    return await points_service.add_points(
        user_id=current_user["id"],
        amount=points_data.amount,
        category=points_data.category,
        description=points_data.description,
        action_source=points_data.action_source
    )


@router.post("/subtract", response_model=UserPointsDetail, status_code=status.HTTP_200_OK)
async def subtract_points(
    points_data: PointsSubtractRequest,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Remove pontos do usuário atual.

    Usado principalmente para resgates de recompensas ou ajustes administrativos.
    """
    points_service = PointsService(db)
    return await points_service.subtract_points(
        user_id=current_user["id"],
        amount=points_data.amount,
        category=points_data.category,
        description=points_data.description,
        action_source=points_data.action_source
    )


@router.get("/categories", response_model=List[str])
async def get_point_categories(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna a lista de categorias de pontos disponíveis.
    """
    points_service = PointsService(db)
    return await points_service.get_point_categories()


@router.get("/user/{user_id}", response_model=UserPointsResponse)
async def get_other_user_points(
    user_id: str = Path(..., description="ID do usuário"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna os pontos de outro usuário.

    Somente administradores podem ver os pontos de outros usuários.
    """
    # Verificar se o usuário atual é administrador
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Somente administradores podem ver pontos de outros usuários"
        )

    points_service = PointsService(db)
    return await points_service.get_user_points(user_id)
