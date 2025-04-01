from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
import logging

from ..models import UserPoint, PointHistory, Achievement, UserAchievement
from ..schemas import UserPointCreate, PointHistoryCreate, AddPointsResponse, AchievementResponse

logger = logging.getLogger(__name__)


class GamificationService:
    def __init__(self, db: Session):
        self.db = db

    # Métodos para Points
    def get_user_points(self, user_id: str) -> UserPoint:
        """Obtém os pontos do usuário, criando um registro se não existir"""
        user_points = self.db.query(UserPoint).filter(
            UserPoint.user_id == user_id).first()
        if not user_points:
            user_points = UserPoint(user_id=user_id, total_points=0)
            self.db.add(user_points)
            self.db.commit()
            self.db.refresh(user_points)
        return user_points

    def add_points(self, user_id: str, amount: int, reason: str) -> AddPointsResponse:
        """Adiciona pontos ao usuário e verifica se novas conquistas foram desbloqueadas"""
        # Verificação de valores negativos ou zero
        if amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A quantidade de pontos deve ser positiva"
            )

        try:
            # Obtém ou cria registro de pontos do usuário
            user_points = self.get_user_points(user_id)

            # Adiciona ao total de pontos
            user_points.total_points += amount

            # Registra histórico
            point_history = PointHistory(
                user_id=user_id,
                amount=amount,
                reason=reason
            )
            self.db.add(point_history)

            # Salva alterações
            self.db.commit()
            self.db.refresh(user_points)

            # Verifica novas conquistas (executado em segundo plano)
            self.check_new_achievements(user_id)

            return AddPointsResponse(
                total_points=user_points.total_points,
                amount_added=amount,
                message=f"{amount} pontos adicionados com sucesso"
            )
        except Exception as e:
            self.db.rollback()
            logger.error(
                f"Erro ao adicionar pontos para usuário {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao adicionar pontos"
            )

    def get_point_history(self, user_id: str) -> List[PointHistory]:
        """Obtém o histórico de pontos do usuário"""
        return self.db.query(PointHistory).filter(
            PointHistory.user_id == user_id
        ).order_by(PointHistory.created_at.desc()).all()

    # Métodos para Achievements
    def get_user_achievements(self, user_id: str) -> List[AchievementResponse]:
        """Obtém todas as conquistas do usuário"""
        results = self.db.query(
            Achievement.id,
            Achievement.badge_name,
            Achievement.description,
            Achievement.category,
            Achievement.icon_url,
            UserAchievement.earned_at
        ).join(
            UserAchievement,
            UserAchievement.achievement_id == Achievement.id
        ).filter(
            UserAchievement.user_id == user_id
        ).order_by(
            UserAchievement.earned_at.desc()
        ).all()

        achievements = []
        for result in results:
            achievements.append(
                AchievementResponse(
                    id=result.id,
                    badge_name=result.badge_name,
                    description=result.description,
                    category=result.category,
                    icon_url=result.icon_url,
                    earned_at=result.earned_at
                )
            )

        return achievements

    def check_new_achievements(self, user_id: str) -> List[AchievementResponse]:
        """Verifica se o usuário desbloqueou novas conquistas"""
        try:
            # Obter pontos atuais e conquistas do usuário
            user_points = self.get_user_points(user_id)
            user_achievement_ids = [
                ua.achievement_id for ua in self.db.query(UserAchievement.achievement_id).filter(
                    UserAchievement.user_id == user_id
                ).all()
            ]

            # Buscar conquistas que o usuário ainda não tem e que podem ser desbloqueadas
            unlockable_achievements = self.db.query(Achievement).filter(
                Achievement.id.notin_(user_achievement_ids),
                Achievement.condition_type == 'points',
                Achievement.points_required <= user_points.total_points
            ).all()

            # Desbloquear novas conquistas
            new_achievements = []
            for achievement in unlockable_achievements:
                user_achievement = UserAchievement(
                    user_id=user_id,
                    achievement_id=achievement.id,
                    notified=0
                )
                self.db.add(user_achievement)
                new_achievements.append(
                    AchievementResponse(
                        id=achievement.id,
                        badge_name=achievement.badge_name,
                        description=achievement.description,
                        category=achievement.category,
                        icon_url=achievement.icon_url,
                        earned_at=func.now()
                    )
                )

                logger.info(
                    f"Usuário {user_id} desbloqueou conquista: {achievement.badge_name}")

            if new_achievements:
                self.db.commit()

            return new_achievements
        except Exception as e:
            self.db.rollback()
            logger.error(
                f"Erro ao verificar conquistas para usuário {user_id}: {str(e)}")
            return []

    def get_new_notifications(self, user_id: str) -> List[AchievementResponse]:
        """Obtém as novas conquistas que ainda não foram notificadas ao usuário"""
        try:
            # Buscar conquistas não notificadas
            results = self.db.query(
                Achievement.id,
                Achievement.badge_name,
                Achievement.description,
                Achievement.category,
                Achievement.icon_url,
                UserAchievement.earned_at,
                UserAchievement.id.label("user_achievement_id")
            ).join(
                Achievement,
                UserAchievement.achievement_id == Achievement.id
            ).filter(
                UserAchievement.user_id == user_id,
                UserAchievement.notified == 0
            ).all()

            # Montar lista de respostas
            notifications = []
            for result in results:
                notifications.append(
                    AchievementResponse(
                        id=result.id,
                        badge_name=result.badge_name,
                        description=result.description,
                        category=result.category,
                        icon_url=result.icon_url,
                        earned_at=result.earned_at
                    )
                )

                # Marcar como notificada
                user_achievement = self.db.query(UserAchievement).filter(
                    UserAchievement.id == result.user_achievement_id
                ).first()

                if user_achievement:
                    user_achievement.notified = 1

            if notifications:
                self.db.commit()

            return notifications
        except Exception as e:
            self.db.rollback()
            logger.error(
                f"Erro ao buscar notificações para usuário {user_id}: {str(e)}")
            return []

    def unlock_achievement_by_condition(
        self, user_id: str, condition_type: str, value: int = 1
    ) -> List[AchievementResponse]:
        """
        Desbloqueia conquistas baseadas em condições específicas como:
        - study_completed
        - chat_used
        - reflection_saved
        - days_streak
        etc.
        """
        try:
            # Obter IDs de conquistas que o usuário já possui
            user_achievement_ids = [
                ua.achievement_id for ua in self.db.query(UserAchievement.achievement_id).filter(
                    UserAchievement.user_id == user_id
                ).all()
            ]

            # Buscar conquistas que podem ser desbloqueadas
            unlockable_achievements = self.db.query(Achievement).filter(
                Achievement.id.notin_(user_achievement_ids),
                Achievement.condition_type == condition_type,
                Achievement.condition_value <= value
            ).all()

            # Desbloquear novas conquistas
            new_achievements = []
            for achievement in unlockable_achievements:
                user_achievement = UserAchievement(
                    user_id=user_id,
                    achievement_id=achievement.id,
                    notified=0
                )
                self.db.add(user_achievement)
                new_achievements.append(
                    AchievementResponse(
                        id=achievement.id,
                        badge_name=achievement.badge_name,
                        description=achievement.description,
                        category=achievement.category,
                        icon_url=achievement.icon_url,
                        earned_at=func.now()
                    )
                )

                logger.info(
                    f"Usuário {user_id} desbloqueou conquista por condição {condition_type}: {achievement.badge_name}")

            if new_achievements:
                self.db.commit()

            return new_achievements
        except Exception as e:
            self.db.rollback()
            logger.error(
                f"Erro ao desbloquear conquistas por condição para usuário {user_id}: {str(e)}")
            return []
