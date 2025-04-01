from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
import logging

from app.models.study_section import StudySection
from app.schemas.study_section import StudySectionCreate, StudySectionUpdate

logger = logging.getLogger(__name__)


class StudySectionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, study_section_create: StudySectionCreate) -> StudySection:
        """
        Cria uma nova seção de estudo.

        Args:
            study_section_create: Dados para criação da seção

        Returns:
            A seção de estudo criada
        """
        study_section = StudySection(**study_section_create.dict())
        self.db.add(study_section)
        await self.db.commit()
        await self.db.refresh(study_section)
        return study_section

    async def create_many(self, study_sections_create: List[StudySectionCreate]) -> List[StudySection]:
        """
        Cria várias seções de estudo.

        Args:
            study_sections_create: Lista de dados para criação de seções

        Returns:
            Lista de seções de estudo criadas
        """
        study_sections = [StudySection(**section.dict())
                          for section in study_sections_create]
        self.db.add_all(study_sections)
        await self.db.commit()

        for section in study_sections:
            await self.db.refresh(section)

        return study_sections

    async def get_by_id(self, section_id: str) -> Optional[StudySection]:
        """
        Obtém uma seção de estudo pelo ID.

        Args:
            section_id: ID da seção

        Returns:
            A seção de estudo ou None se não for encontrada
        """
        result = await self.db.execute(
            select(StudySection).where(StudySection.id == section_id)
        )
        return result.scalars().first()

    async def get_by_plan_id(self, plan_id: str) -> List[StudySection]:
        """
        Obtém todas as seções de um plano de estudo.

        Args:
            plan_id: ID do plano

        Returns:
            Lista de seções do plano
        """
        result = await self.db.execute(
            select(StudySection)
            .where(StudySection.study_plan_id == plan_id)
            .order_by(StudySection.position)
        )
        return result.scalars().all()

    async def update(self, section_id: str, section_update: StudySectionUpdate) -> Optional[StudySection]:
        """
        Atualiza uma seção de estudo.

        Args:
            section_id: ID da seção
            section_update: Dados para atualização

        Returns:
            A seção atualizada ou None se não for encontrada
        """
        update_data = section_update.dict(exclude_unset=True)

        await self.db.execute(
            update(StudySection)
            .where(StudySection.id == section_id)
            .values(**update_data)
        )
        await self.db.commit()

        return await self.get_by_id(section_id)

    async def delete(self, section_id: str) -> bool:
        """
        Exclui uma seção de estudo.

        Args:
            section_id: ID da seção

        Returns:
            True se a seção foi excluída, False caso contrário
        """
        result = await self.db.execute(
            delete(StudySection).where(StudySection.id == section_id)
        )
        await self.db.commit()

        return result.rowcount > 0

    async def delete_by_plan_id(self, plan_id: str) -> int:
        """
        Exclui todas as seções de um plano de estudo.

        Args:
            plan_id: ID do plano

        Returns:
            Número de seções excluídas
        """
        result = await self.db.execute(
            delete(StudySection).where(StudySection.study_plan_id == plan_id)
        )
        await self.db.commit()

        return result.rowcount
