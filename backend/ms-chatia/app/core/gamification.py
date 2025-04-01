"""
Serviço de gamificação do sistema FaleComJesus.

Este módulo implementa o sistema de gamificação que incentiva
e recompensa o engajamento dos usuários na plataforma.

Features:
    - Pontos por atividades
    - Conquistas e selos
    - Níveis de progresso
    - Recompensas diárias
    - Rankings semanais
    - Certificados especiais
"""

from typing import Dict, List, Optional, Union
import logging
from datetime import datetime, timedelta
from .config import settings
from .cache import cache
from .metrics import metrics
from .database import db

# Logger
logger = logging.getLogger(__name__)


class GamificationManager:
    """
    Gerenciador de gamificação.

    Features:
        - Pontuação
        - Conquistas
        - Níveis
        - Recompensas
        - Rankings

    Attributes:
        points_per_activity: Pontos por atividade
        achievements: Lista de conquistas
        levels: Níveis de progresso
        metrics: Métricas de gamificação
    """

    def __init__(
        self,
        points_per_activity: Optional[Dict] = None,
        achievements: Optional[List] = None,
        levels: Optional[List] = None
    ):
        """
        Inicializa o gerenciador de gamificação.

        Args:
            points_per_activity: Pontos por atividade
            achievements: Lista de conquistas
            levels: Níveis de progresso
        """
        # Configurações
        self.points_per_activity = points_per_activity or {
            "study_completed": 100,
            "reflection_added": 50,
            "chat_message": 10,
            "daily_login": 20,
            "certificate_earned": 200
        }

        self.achievements = achievements or [
            {
                "id": "first_study",
                "name": "Primeiro Passo",
                "description": "Complete seu primeiro estudo",
                "points": 100,
                "icon": "🎯"
            },
            {
                "id": "seven_days",
                "name": "Constância",
                "description": "Estude por 7 dias consecutivos",
                "points": 500,
                "icon": "🔥"
            },
            {
                "id": "master",
                "name": "Mestre",
                "description": "Complete 10 planos de estudo",
                "points": 1000,
                "icon": "👑"
            }
        ]

        self.levels = levels or [
            {"level": 1, "points": 0, "name": "Iniciante"},
            {"level": 2, "points": 500, "name": "Aprendiz"},
            {"level": 3, "points": 1000, "name": "Discípulo"},
            {"level": 4, "points": 2000, "name": "Mestre"},
            {"level": 5, "points": 5000, "name": "Sábio"}
        ]

        logger.info("Gerenciador de gamificação inicializado")

    async def add_points(
        self,
        user_id: str,
        activity: str,
        points: Optional[int] = None
    ) -> Dict:
        """
        Adiciona pontos por atividade.

        Args:
            user_id: ID do usuário
            activity: Tipo de atividade
            points: Pontos (opcional)

        Returns:
            Dict: Resultado da pontuação
        """
        try:
            # Valida atividade
            if activity not in self.points_per_activity:
                raise ValueError(f"Atividade inválida: {activity}")

            # Pontos da atividade
            activity_points = points or self.points_per_activity[activity]

            # Adiciona pontos
            result = await self._add_points_to_user(
                user_id,
                activity_points
            )

            # Verifica conquistas
            await self._check_achievements(user_id)

            # Registra métricas
            metrics.track_gamification(
                "points_added",
                activity=activity,
                points=activity_points
            )

            return result

        except Exception as e:
            logger.error(f"Erro ao adicionar pontos: {str(e)}")
            raise

    async def get_achievements(
        self,
        user_id: str
    ) -> List[Dict]:
        """
        Retorna conquistas do usuário.

        Args:
            user_id: ID do usuário

        Returns:
            List[Dict]: Lista de conquistas
        """
        try:
            # Busca conquistas
            achievements = await self._get_user_achievements(user_id)

            # Formata resultado
            result = []
            for achievement in self.achievements:
                result.append({
                    **achievement,
                    "earned": achievement["id"] in achievements
                })

            return result

        except Exception as e:
            logger.error(f"Erro ao buscar conquistas: {str(e)}")
            return []

    async def get_level(
        self,
        user_id: str
    ) -> Dict:
        """
        Retorna nível atual do usuário.

        Args:
            user_id: ID do usuário

        Returns:
            Dict: Dados do nível
        """
        try:
            # Busca pontos
            points = await self._get_user_points(user_id)

            # Calcula nível
            current_level = None
            next_level = None

            for i, level in enumerate(self.levels):
                if points >= level["points"]:
                    current_level = level
                    if i < len(self.levels) - 1:
                        next_level = self.levels[i + 1]

            return {
                "current": current_level,
                "next": next_level,
                "points": points,
                "progress": self._calculate_progress(
                    points,
                    current_level,
                    next_level
                )
            }

        except Exception as e:
            logger.error(f"Erro ao calcular nível: {str(e)}")
            return {
                "current": self.levels[0],
                "next": self.levels[1],
                "points": 0,
                "progress": 0
            }

    async def get_weekly_ranking(
        self,
        limit: int = 10
    ) -> List[Dict]:
        """
        Retorna ranking semanal.

        Args:
            limit: Limite de usuários

        Returns:
            List[Dict]: Lista de usuários
        """
        try:
            # Busca ranking
            ranking = await self._get_weekly_ranking(limit)

            # Formata resultado
            result = []
            for i, user in enumerate(ranking, 1):
                result.append({
                    "position": i,
                    "user_id": user["user_id"],
                    "user_name": user["user_name"],
                    "points": user["points"],
                    "level": await self.get_level(user["user_id"])
                })

            return result

        except Exception as e:
            logger.error(f"Erro ao buscar ranking: {str(e)}")
            return []

    async def _add_points_to_user(
        self,
        user_id: str,
        points: int
    ) -> Dict:
        """
        Adiciona pontos ao usuário.

        Args:
            user_id: ID do usuário
            points: Pontos

        Returns:
            Dict: Resultado
        """
        try:
            # Busca pontos atuais
            current_points = await self._get_user_points(user_id)

            # Adiciona pontos
            new_points = current_points + points

            # Atualiza no banco
            await self._update_user_points(
                user_id,
                new_points
            )

            return {
                "user_id": user_id,
                "points_added": points,
                "total_points": new_points
            }

        except Exception as e:
            logger.error(f"Erro ao atualizar pontos: {str(e)}")
            raise

    async def _check_achievements(
        self,
        user_id: str
    ) -> List[Dict]:
        """
        Verifica conquistas do usuário.

        Args:
            user_id: ID do usuário

        Returns:
            List[Dict]: Conquistas desbloqueadas
        """
        try:
            # Busca conquistas atuais
            current = await self._get_user_achievements(user_id)

            # Verifica novas conquistas
            new_achievements = []

            for achievement in self.achievements:
                if achievement["id"] not in current:
                    # Verifica critérios
                    if await self._check_achievement_criteria(
                        user_id,
                        achievement
                    ):
                        # Desbloqueia conquista
                        await self._unlock_achievement(
                            user_id,
                            achievement
                        )

                        new_achievements.append(achievement)

            return new_achievements

        except Exception as e:
            logger.error(f"Erro ao verificar conquistas: {str(e)}")
            return []

    async def _check_achievement_criteria(
        self,
        user_id: str,
        achievement: Dict
    ) -> bool:
        """
        Verifica critérios da conquista.

        Args:
            user_id: ID do usuário
            achievement: Dados da conquista

        Returns:
            bool: True se atende critérios
        """
        try:
            # Critérios por conquista
            criteria = {
                "first_study": lambda: self._check_first_study(user_id),
                "seven_days": lambda: self._check_streak(user_id, 7),
                "master": lambda: self._check_completed_plans(user_id, 10)
            }

            # Verifica critério
            if achievement["id"] in criteria:
                return await criteria[achievement["id"]]()

            return False

        except Exception as e:
            logger.error(f"Erro ao verificar critérios: {str(e)}")
            return False

    def _calculate_progress(
        self,
        points: int,
        current_level: Dict,
        next_level: Optional[Dict]
    ) -> float:
        """
        Calcula progresso para próximo nível.

        Args:
            points: Pontos atuais
            current_level: Nível atual
            next_level: Próximo nível

        Returns:
            float: Progresso (0-100)
        """
        try:
            if not next_level:
                return 100

            # Pontos necessários
            points_needed = next_level["points"] - current_level["points"]
            points_current = points - current_level["points"]

            # Calcula porcentagem
            return (points_current / points_needed) * 100

        except Exception as e:
            logger.error(f"Erro ao calcular progresso: {str(e)}")
            return 0


# Instância global de gamificação
gamification = GamificationManager()
