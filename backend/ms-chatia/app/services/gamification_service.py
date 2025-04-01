import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.gamification import UserPoints, UserAchievement
from app.schemas.gamification import AchievementCreate

logger = logging.getLogger(__name__)


class GamificationService:
    """
    Serviço para gerenciamento de gamificação.

    Responsável por:
    - Controlar pontos dos usuários
    - Gerenciar conquistas e selos
    - Calcular progresso e níveis
    - Distribuir recompensas

    Attributes:
        db: Sessão do banco de dados
        redis: Cliente Redis para cache
    """

    def __init__(self, db: Session):
        """
        Inicializa o serviço de gamificação.

        Args:
            db: Sessão do banco de dados
        """
        self.db = db

    async def add_points(
        self,
        user_id: UUID,
        points: int,
        reason: str
    ) -> Dict:
        """
        Adiciona pontos ao usuário.

        Args:
            user_id: ID do usuário
            points: Quantidade de pontos
            reason: Motivo da pontuação

        Returns:
            Dict com total atual

        Raises:
            HTTPException: Se erro ao adicionar
        """
        try:
            # Busca ou cria registro de pontos
            user_points = self.db.query(UserPoints).filter(
                UserPoints.user_id == user_id
            ).first()

            if not user_points:
                user_points = UserPoints(
                    user_id=user_id,
                    total_points=0
                )
                self.db.add(user_points)

            # Atualiza pontos
            user_points.total_points += points
            user_points.last_updated = datetime.utcnow()

            self.db.commit()
            self.db.refresh(user_points)

            # Verifica conquistas por pontos
            await self.check_point_achievements(user_id, user_points.total_points)

            return {
                "total_points": user_points.total_points,
                "points_added": points,
                "reason": reason,
                "timestamp": datetime.utcnow()
            }

        except Exception as e:
            logger.error(f"Error adding points: {str(e)}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao adicionar pontos"
            )

    async def get_user_points(
        self,
        user_id: UUID
    ) -> Dict:
        """
        Retorna pontuação do usuário.

        Args:
            user_id: ID do usuário

        Returns:
            Dict com pontos e nível

        Raises:
            HTTPException: Se erro na consulta
        """
        try:
            user_points = self.db.query(UserPoints).filter(
                UserPoints.user_id == user_id
            ).first()

            if not user_points:
                return {
                    "total_points": 0,
                    "level": 1,
                    "next_level": 100,
                    "progress": 0
                }

            # Calcula nível atual
            level = 1 + (user_points.total_points // 100)
            next_level = level * 100
            progress = (user_points.total_points % 100) / 100

            return {
                "total_points": user_points.total_points,
                "level": level,
                "next_level": next_level,
                "progress": progress
            }

        except Exception as e:
            logger.error(f"Error getting points: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao buscar pontuação"
            )

    async def unlock_achievement(
        self,
        user_id: UUID,
        badge_name: str,
        description: str,
        points: int = 0
    ) -> Dict:
        """
        Desbloqueia conquista para usuário.

        Args:
            user_id: ID do usuário
            badge_name: Nome do selo
            description: Descrição da conquista
            points: Pontos bônus

        Returns:
            Dict com detalhes da conquista

        Raises:
            HTTPException: Se erro ao desbloquear
        """
        try:
            # Verifica se já possui
            existing = self.db.query(UserAchievement).filter(
                UserAchievement.user_id == user_id,
                UserAchievement.badge_name == badge_name
            ).first()

            if existing:
                return {
                    "id": existing.id,
                    "badge_name": existing.badge_name,
                    "description": existing.description,
                    "earned_at": existing.earned_at
                }

            # Cria nova conquista
            achievement = UserAchievement(
                user_id=user_id,
                badge_name=badge_name,
                description=description,
                earned_at=datetime.utcnow()
            )

            self.db.add(achievement)
            self.db.commit()
            self.db.refresh(achievement)

            # Adiciona pontos bônus
            if points > 0:
                await self.add_points(
                    user_id=user_id,
                    points=points,
                    reason=f"Conquista: {badge_name}"
                )

            return {
                "id": achievement.id,
                "badge_name": achievement.badge_name,
                "description": achievement.description,
                "earned_at": achievement.earned_at,
                "bonus_points": points
            }

        except Exception as e:
            logger.error(f"Error unlocking achievement: {str(e)}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao desbloquear conquista"
            )

    async def get_achievements(
        self,
        user_id: UUID
    ) -> List[Dict]:
        """
        Lista conquistas do usuário.

        Args:
            user_id: ID do usuário

        Returns:
            Lista de conquistas

        Raises:
            HTTPException: Se erro na consulta
        """
        try:
            achievements = self.db.query(UserAchievement).filter(
                UserAchievement.user_id == user_id
            ).order_by(UserAchievement.earned_at.desc()).all()

            return [{
                "id": a.id,
                "badge_name": a.badge_name,
                "description": a.description,
                "earned_at": a.earned_at
            } for a in achievements]

        except Exception as e:
            logger.error(f"Error getting achievements: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao buscar conquistas"
            )

    async def check_point_achievements(
        self,
        user_id: UUID,
        total_points: int
    ) -> None:
        """
        Verifica conquistas por pontuação.

        Args:
            user_id: ID do usuário
            total_points: Total de pontos

        Raises:
            HTTPException: Se erro na verificação
        """
        try:
            # Conquistas por pontos
            if total_points >= 1000:
                await self.unlock_achievement(
                    user_id=user_id,
                    badge_name="Mestre Espiritual",
                    description="Alcançou 1000 pontos de sabedoria",
                    points=100
                )
            elif total_points >= 500:
                await self.unlock_achievement(
                    user_id=user_id,
                    badge_name="Discípulo Dedicado",
                    description="Alcançou 500 pontos de sabedoria",
                    points=50
                )
            elif total_points >= 100:
                await self.unlock_achievement(
                    user_id=user_id,
                    badge_name="Iniciante Inspirado",
                    description="Alcançou 100 pontos de sabedoria",
                    points=10
                )

        except Exception as e:
            logger.error(f"Error checking achievements: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao verificar conquistas"
            )

    async def get_leaderboard(
        self,
        user_id: UUID
    ) -> Dict:
        """
        Retorna ranking pessoal do usuário.

        Args:
            user_id: ID do usuário

        Returns:
            Dict com posição e pontos

        Raises:
            HTTPException: Se erro na consulta
        """
        try:
            # Busca pontuação do usuário
            user_points = await self.get_user_points(user_id)

            # Conta usuários com mais pontos
            position = self.db.query(UserPoints).filter(
                UserPoints.total_points > user_points["total_points"]
            ).count() + 1

            return {
                "position": position,
                "total_points": user_points["total_points"],
                "level": user_points["level"],
                "next_level": user_points["next_level"],
                "progress": user_points["progress"]
            }

        except Exception as e:
            logger.error(f"Error getting leaderboard: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao buscar ranking"
            )
