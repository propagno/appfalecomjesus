from typing import Dict, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.logging import get_logger
from app.schemas.gamification import (
    UserPoints,
    Achievement,
    AchievementProgress,
    LeaderboardEntry
)
from app.services.gamification_service import GamificationService

router = APIRouter()
logger = get_logger(__name__)


@router.get(
    "/points",
    response_model=UserPoints,
    summary="Pontuação do usuário",
    description="""
    Retorna a pontuação atual do usuário.
    
    Inclui:
    - Total de pontos
    - Nível atual
    - Pontos para próximo nível
    - Histórico de pontos ganhos
    """
)
async def get_user_points(
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> UserPoints:
    """
    Retorna a pontuação do usuário.

    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        UserPoints com detalhes da pontuação

    Raises:
        HTTPException: Se erro ao buscar pontos
    """
    try:
        gamification_service = GamificationService(db)
        return await gamification_service.get_user_points(
            user_id=current_user["id"]
        )
    except Exception as e:
        logger.error(f"Error getting user points: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar pontuação"
        )


@router.get(
    "/achievements",
    response_model=List[Achievement],
    summary="Conquistas do usuário",
    description="""
    Lista todas as conquistas do usuário.
    
    Inclui conquistas:
    - Desbloqueadas
    - Em progresso
    - Bloqueadas
    
    Cada conquista tem:
    - Nome
    - Descrição
    - Data de desbloqueio
    - Pontos recebidos
    """
)
async def list_achievements(
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> List[Achievement]:
    """
    Lista conquistas do usuário.

    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Lista de Achievement

    Raises:
        HTTPException: Se erro ao listar
    """
    try:
        gamification_service = GamificationService(db)
        return await gamification_service.list_achievements(
            user_id=current_user["id"]
        )
    except Exception as e:
        logger.error(f"Error listing achievements: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar conquistas"
        )


@router.get(
    "/achievements/{achievement_id}/progress",
    response_model=AchievementProgress,
    summary="Progresso da conquista",
    description="""
    Retorna o progresso em uma conquista específica.
    
    Inclui:
    - Porcentagem completada
    - Requisitos cumpridos
    - Requisitos pendentes
    - Estimativa para conclusão
    """
)
async def get_achievement_progress(
    achievement_id: UUID,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> AchievementProgress:
    """
    Retorna progresso em uma conquista.

    Args:
        achievement_id: ID da conquista
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        AchievementProgress com detalhes

    Raises:
        HTTPException: Se conquista não encontrada
    """
    try:
        gamification_service = GamificationService(db)
        return await gamification_service.get_achievement_progress(
            user_id=current_user["id"],
            achievement_id=achievement_id
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting achievement progress: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar progresso"
        )


@router.get(
    "/leaderboard",
    response_model=List[LeaderboardEntry],
    summary="Ranking pessoal",
    description="""
    Retorna o ranking pessoal do usuário.
    
    Mostra:
    - Posição atual
    - Pontuação
    - Nível
    - Conquistas desbloqueadas
    - Progresso semanal
    
    Não exibe outros usuários.
    """
)
async def get_leaderboard(
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> List[LeaderboardEntry]:
    """
    Retorna ranking pessoal.

    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Lista de LeaderboardEntry

    Raises:
        HTTPException: Se erro ao buscar ranking
    """
    try:
        gamification_service = GamificationService(db)
        return await gamification_service.get_leaderboard(
            user_id=current_user["id"]
        )
    except Exception as e:
        logger.error(f"Error getting leaderboard: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar ranking"
        )


@router.post(
    "/points/bonus",
    response_model=UserPoints,
    summary="Adicionar pontos bônus",
    description="""
    Adiciona pontos bônus ao usuário.
    
    Pontos são dados por:
    - Assistir anúncios (plano Free)
    - Compartilhar certificados
    - Completar desafios diários
    - Manter sequência de estudos
    """
)
async def add_bonus_points(
    points: int,
    reason: str,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> UserPoints:
    """
    Adiciona pontos bônus.

    Args:
        points: Quantidade de pontos
        reason: Motivo do bônus
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        UserPoints atualizado

    Raises:
        HTTPException: Se erro ao adicionar
    """
    try:
        gamification_service = GamificationService(db)
        return await gamification_service.add_bonus_points(
            user_id=current_user["id"],
            points=points,
            reason=reason
        )
    except Exception as e:
        logger.error(f"Error adding bonus points: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao adicionar pontos"
        )
