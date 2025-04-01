from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
import logging

from app.models.study_plan import StudyPlan
from app.schemas.study_plan import StudyPlanCreate, StudyPlanUpdate

logger = logging.getLogger(__name__)


class StudyPlanRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, study_plan_create: StudyPlanCreate) -> StudyPlan:
        """
        Cria um novo plano de estudo.

        Args:
            study_plan_create: Dados para criação do plano

        Returns:
            O plano de estudo criado
        """
        study_plan = StudyPlan(**study_plan_create.dict())
        self.db.add(study_plan)
        await self.db.commit()
        await self.db.refresh(study_plan)
        return study_plan

    async def get_by_id(self, study_plan_id: str) -> Optional[StudyPlan]:
        """
        Obtém um plano de estudo pelo ID.

        Args:
            study_plan_id: ID do plano

        Returns:
            O plano de estudo ou None se não for encontrado
        """
        result = await self.db.execute(
            select(StudyPlan).where(StudyPlan.id == study_plan_id)
        )
        return result.scalars().first()

    async def get_all(self) -> List[StudyPlan]:
        """
        Obtém todos os planos de estudo.

        Returns:
            Lista de planos de estudo
        """
        result = await self.db.execute(select(StudyPlan))
        return result.scalars().all()

    async def get_by_user_id(self, user_id: str) -> List[StudyPlan]:
        """
        Obtém todos os planos de estudo de um usuário.

        Args:
            user_id: ID do usuário

        Returns:
            Lista de planos de estudo do usuário
        """
        result = await self.db.execute(
            select(StudyPlan).where(StudyPlan.user_id == user_id)
        )
        return result.scalars().all()

    async def update(self, study_plan_id: str, study_plan_update: StudyPlanUpdate) -> Optional[StudyPlan]:
        """
        Atualiza um plano de estudo.

        Args:
            study_plan_id: ID do plano
            study_plan_update: Dados para atualização

        Returns:
            O plano atualizado ou None se não for encontrado
        """
        update_data = study_plan_update.dict(exclude_unset=True)

        await self.db.execute(
            update(StudyPlan)
            .where(StudyPlan.id == study_plan_id)
            .values(**update_data)
        )
        await self.db.commit()

        return await self.get_by_id(study_plan_id)

    async def delete(self, study_plan_id: str) -> bool:
        """
        Exclui um plano de estudo.

        Args:
            study_plan_id: ID do plano

        Returns:
            True se o plano foi excluído, False caso contrário
        """
        result = await self.db.execute(
            delete(StudyPlan).where(StudyPlan.id == study_plan_id)
        )
        await self.db.commit()

        return result.rowcount > 0
