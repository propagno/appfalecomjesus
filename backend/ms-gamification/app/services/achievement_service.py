from datetime import datetime
from typing import List, Dict, Optional, Any
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import and_, desc, asc

from app.models.achievement import Achievement
from app.models.user_achievement import UserAchievement
from app.schemas.gamification import (
    AchievementResponse,
    AchievementListResponse,
    UserAchievementResponse,
    UserAchievementDetail,
    AchievementProgressDetail
)


class AchievementService:
    """Serviço para gerenciamento de conquistas e progresso dos usuários"""

    def __init__(self, db: Session):
        self.db = db

        # Categorias válidas de conquistas
        self._valid_categories = [
            "oracao",
            "estudo",
            "compartilhamento",
            "assiduidade",
            "contribuicao",
            "reflexao",
            "comunidade"
        ]

        # Dificuldades válidas
        self._valid_difficulties = [
            "facil",
            "medio",
            "dificil",
            "especialista"
        ]

    async def get_achievements(
        self,
        skip: int = 0,
        limit: int = 10,
        category: Optional[str] = None,
        difficulty: Optional[str] = None
    ) -> AchievementListResponse:
        """
        Lista todas as conquistas disponíveis no sistema.

        Args:
            skip: Quantos registros pular (para paginação)
            limit: Limite de registros a retornar
            category: Filtrar por categoria específica
            difficulty: Filtrar por nível de dificuldade

        Returns:
            Lista paginada de conquistas
        """
        # Construir a query base
        query = self.db.query(Achievement)

        # Aplicar filtros
        if category:
            query = query.filter(Achievement.category == category)

        if difficulty:
            query = query.filter(Achievement.difficulty == difficulty)

        # Obter o total para paginação
        total = query.count()

        # Aplicar ordenação e paginação
        query = query.order_by(
            Achievement.difficulty,
            Achievement.points_required
        ).offset(skip).limit(limit)

        # Executar a consulta
        achievements = query.all()

        # Criar a resposta
        items = [
            AchievementResponse(
                id=ach.id,
                title=ach.title,
                description=ach.description,
                category=ach.category,
                difficulty=ach.difficulty,
                points_required=ach.points_required,
                icon_url=ach.icon_url,
                badge_url=ach.badge_url,
                unlocked_users=ach.unlocked_users,
                created_at=ach.created_at
            ) for ach in achievements
        ]

        return AchievementListResponse(
            items=items,
            total=total,
            skip=skip,
            limit=limit
        )

    async def get_achievement_by_id(self, achievement_id: str) -> AchievementResponse:
        """
        Obtém detalhes de uma conquista específica.

        Args:
            achievement_id: ID da conquista

        Returns:
            Detalhes da conquista

        Raises:
            ValueError: Se a conquista não for encontrada
        """
        achievement = self.db.query(Achievement).filter(
            Achievement.id == achievement_id
        ).first()

        if not achievement:
            raise ValueError(f"Conquista não encontrada: {achievement_id}")

        return AchievementResponse(
            id=achievement.id,
            title=achievement.title,
            description=achievement.description,
            category=achievement.category,
            difficulty=achievement.difficulty,
            points_required=achievement.points_required,
            icon_url=achievement.icon_url,
            badge_url=achievement.badge_url,
            unlocked_users=achievement.unlocked_users,
            created_at=achievement.created_at
        )

    async def get_user_achievements(self, user_id: str) -> UserAchievementResponse:
        """
        Obtém as conquistas de um usuário específico.

        Args:
            user_id: ID do usuário

        Returns:
            Resposta com conquistas do usuário
        """
        # Buscar conquistas que o usuário já desbloqueou
        unlocked_query = self.db.query(
            Achievement, UserAchievement
        ).join(
            UserAchievement,
            Achievement.id == UserAchievement.achievement_id
        ).filter(
            UserAchievement.user_id == user_id,
            UserAchievement.is_unlocked == True
        ).order_by(
            desc(UserAchievement.unlocked_at)
        ).all()

        # Buscar todas as conquistas para calcular o progresso
        all_achievements = self.db.query(Achievement).all()

        # Mapear conquistas desbloqueadas para rápido acesso
        unlocked_map = {item[0].id: item[1] for item in unlocked_query}

        # Calcular progresso
        total_achievements = len(all_achievements)
        unlocked_achievements = len(unlocked_map)
        completion_percentage = int(
            (unlocked_achievements / total_achievements * 100) if total_achievements > 0 else 0)

        # Preparar conquistas desbloqueadas
        unlocked = [
            UserAchievementDetail(
                id=item[0].id,
                title=item[0].title,
                description=item[0].description,
                category=item[0].category,
                difficulty=item[0].difficulty,
                icon_url=item[0].icon_url,
                badge_url=item[0].badge_url,
                unlocked_at=item[1].unlocked_at
            ) for item in unlocked_query
        ]

        # Preparar conquistas em progresso (ainda não desbloqueadas)
        in_progress = []
        for ach in all_achievements:
            if ach.id not in unlocked_map:
                # Obtém o progresso atual do usuário para esta conquista
                progress = await self.get_user_achievement_progress(user_id, ach.id)

                in_progress.append(AchievementProgressDetail(
                    id=ach.id,
                    title=ach.title,
                    description=ach.description,
                    category=ach.category,
                    difficulty=ach.difficulty,
                    points_required=ach.points_required,
                    current_points=progress.get("current_points", 0),
                    percentage=progress.get("percentage", 0),
                    icon_url=ach.icon_url
                ))

        # Ordenar conquistas em progresso por porcentagem de conclusão (decrescente)
        in_progress.sort(key=lambda x: x.percentage, reverse=True)

        # Preparar conquistas recentes (últimas 5 desbloqueadas)
        recent = unlocked[:5] if unlocked else []

        return UserAchievementResponse(
            user_id=user_id,
            total_achievements=total_achievements,
            unlocked_achievements=unlocked_achievements,
            completion_percentage=completion_percentage,
            unlocked=unlocked,
            in_progress=in_progress,
            recent=recent
        )

    async def get_user_achievement_progress(
        self,
        user_id: str,
        achievement_id: str
    ) -> Dict[str, Any]:
        """
        Calcula o progresso atual do usuário para uma conquista específica.

        Args:
            user_id: ID do usuário
            achievement_id: ID da conquista

        Returns:
            Dicionário com informações de progresso
        """
        # Buscar a conquista
        achievement = self.db.query(Achievement).filter(
            Achievement.id == achievement_id
        ).first()

        if not achievement:
            return {
                "current_points": 0,
                "required_points": 0,
                "percentage": 0
            }

        # Verificar se já existe um registro de progresso
        user_achievement = self.db.query(UserAchievement).filter(
            and_(
                UserAchievement.user_id == user_id,
                UserAchievement.achievement_id == achievement_id
            )
        ).first()

        # Se não existir, criar um novo com progresso zero
        if not user_achievement:
            user_achievement = UserAchievement(
                id=str(uuid4()),
                user_id=user_id,
                achievement_id=achievement_id,
                current_points=0,
                is_unlocked=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                unlocked_at=None
            )
            self.db.add(user_achievement)
            self.db.commit()

        # Calcular porcentagem
        percentage = int((user_achievement.current_points / achievement.points_required * 100)
                         if achievement.points_required > 0 else 0)
        percentage = min(percentage, 100)  # Limitar a 100%

        return {
            "current_points": user_achievement.current_points,
            "required_points": achievement.points_required,
            "percentage": percentage
        }

    async def update_achievement_progress(
        self,
        user_id: str,
        achievement_id: str,
        points_to_add: int
    ) -> Dict[str, Any]:
        """
        Atualiza o progresso de um usuário em uma conquista.

        Args:
            user_id: ID do usuário
            achievement_id: ID da conquista
            points_to_add: Pontos a adicionar ao progresso

        Returns:
            Dicionário com progresso atualizado e status de desbloqueio
        """
        # Buscar a conquista
        achievement = self.db.query(Achievement).filter(
            Achievement.id == achievement_id
        ).first()

        if not achievement:
            raise ValueError(f"Conquista não encontrada: {achievement_id}")

        # Buscar o progresso atual
        user_achievement = self.db.query(UserAchievement).filter(
            and_(
                UserAchievement.user_id == user_id,
                UserAchievement.achievement_id == achievement_id
            )
        ).first()

        # Se não existir, criar um novo
        if not user_achievement:
            user_achievement = UserAchievement(
                id=str(uuid4()),
                user_id=user_id,
                achievement_id=achievement_id,
                current_points=0,
                is_unlocked=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                unlocked_at=None
            )
            self.db.add(user_achievement)

        # Verificar se já está desbloqueada
        newly_unlocked = False
        if user_achievement.is_unlocked:
            # Já desbloqueada, não precisa atualizar
            return {
                "is_unlocked": True,
                "newly_unlocked": False,
                "current_points": user_achievement.current_points,
                "required_points": achievement.points_required,
                "percentage": 100
            }

        # Atualizar pontos
        user_achievement.current_points += points_to_add
        user_achievement.updated_at = datetime.utcnow()

        # Verificar se desbloqueou
        if user_achievement.current_points >= achievement.points_required:
            user_achievement.is_unlocked = True
            user_achievement.unlocked_at = datetime.utcnow()
            newly_unlocked = True

            # Atualizar contagem de usuários que desbloquearam
            achievement.unlocked_users += 1

        # Calcular porcentagem
        percentage = int((user_achievement.current_points / achievement.points_required * 100)
                         if achievement.points_required > 0 else 0)
        percentage = min(percentage, 100)  # Limitar a 100%

        self.db.commit()

        return {
            "is_unlocked": user_achievement.is_unlocked,
            "newly_unlocked": newly_unlocked,
            "current_points": user_achievement.current_points,
            "required_points": achievement.points_required,
            "percentage": percentage
        }

    async def check_achievement(
        self,
        user_id: str,
        achievement_id: str
    ) -> AchievementResponse:
        """
        Verifica e atualiza o status de uma conquista para um usuário.

        Esta função é chamada explicitamente para verificar conquistas que
        não são automaticamente verificadas pelo sistema.

        Args:
            user_id: ID do usuário
            achievement_id: ID da conquista

        Returns:
            Detalhes da conquista com status atualizado
        """
        # Buscar a conquista
        achievement = self.db.query(Achievement).filter(
            Achievement.id == achievement_id
        ).first()

        if not achievement:
            raise ValueError(f"Conquista não encontrada: {achievement_id}")

        # TODO: Implementar lógica específica para verificar os requisitos
        # Esta é uma implementação simplificada para demonstração

        # Obtém o progresso atual
        progress = await self.get_user_achievement_progress(user_id, achievement_id)

        # Retorna detalhes da conquista com o progresso
        response = AchievementResponse(
            id=achievement.id,
            title=achievement.title,
            description=achievement.description,
            category=achievement.category,
            difficulty=achievement.difficulty,
            points_required=achievement.points_required,
            icon_url=achievement.icon_url,
            badge_url=achievement.badge_url,
            unlocked_users=achievement.unlocked_users,
            created_at=achievement.created_at,
            user_progress=progress
        )

        return response

    async def get_achievement_categories(self) -> List[str]:
        """
        Retorna a lista de categorias de conquistas disponíveis.

        Returns:
            Lista de categorias válidas
        """
        return self._valid_categories
