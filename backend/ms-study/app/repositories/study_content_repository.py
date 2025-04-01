from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
import logging

from app.models.study_content import StudyContent
from app.schemas.study_content import StudyContentCreate, StudyContentUpdate

logger = logging.getLogger(__name__)


class StudyContentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, study_content_create: StudyContentCreate) -> StudyContent:
        """
        Cria um novo conteúdo de estudo.

        Args:
            study_content_create: Dados para criação do conteúdo

        Returns:
            O conteúdo de estudo criado
        """
        study_content = StudyContent(**study_content_create.dict())
        self.db.add(study_content)
        await self.db.commit()
        await self.db.refresh(study_content)
        return study_content

    async def create_many(self, study_contents_create: List[StudyContentCreate]) -> List[StudyContent]:
        """
        Cria vários conteúdos de estudo.

        Args:
            study_contents_create: Lista de dados para criação de conteúdos

        Returns:
            Lista de conteúdos de estudo criados
        """
        study_contents = [StudyContent(**content.dict())
                          for content in study_contents_create]
        self.db.add_all(study_contents)
        await self.db.commit()

        for content in study_contents:
            await self.db.refresh(content)

        return study_contents

    async def get_by_id(self, content_id: str) -> Optional[StudyContent]:
        """
        Obtém um conteúdo de estudo pelo ID.

        Args:
            content_id: ID do conteúdo

        Returns:
            O conteúdo de estudo ou None se não for encontrado
        """
        result = await self.db.execute(
            select(StudyContent).where(StudyContent.id == content_id)
        )
        return result.scalars().first()

    async def get_by_section_id(self, section_id: str) -> List[StudyContent]:
        """
        Obtém todos os conteúdos de uma seção de estudo.

        Args:
            section_id: ID da seção

        Returns:
            Lista de conteúdos da seção
        """
        result = await self.db.execute(
            select(StudyContent)
            .where(StudyContent.section_id == section_id)
            .order_by(StudyContent.position)
        )
        return result.scalars().all()

    async def update(self, content_id: str, content_update: StudyContentUpdate) -> Optional[StudyContent]:
        """
        Atualiza um conteúdo de estudo.

        Args:
            content_id: ID do conteúdo
            content_update: Dados para atualização

        Returns:
            O conteúdo atualizado ou None se não for encontrado
        """
        update_data = content_update.dict(exclude_unset=True)

        await self.db.execute(
            update(StudyContent)
            .where(StudyContent.id == content_id)
            .values(**update_data)
        )
        await self.db.commit()

        return await self.get_by_id(content_id)

    async def delete(self, content_id: str) -> bool:
        """
        Exclui um conteúdo de estudo.

        Args:
            content_id: ID do conteúdo

        Returns:
            True se o conteúdo foi excluído, False caso contrário
        """
        result = await self.db.execute(
            delete(StudyContent).where(StudyContent.id == content_id)
        )
        await self.db.commit()

        return result.rowcount > 0

    async def delete_by_section_id(self, section_id: str) -> int:
        """
        Exclui todos os conteúdos de uma seção de estudo.

        Args:
            section_id: ID da seção

        Returns:
            Número de conteúdos excluídos
        """
        result = await self.db.execute(
            delete(StudyContent).where(StudyContent.section_id == section_id)
        )
        await self.db.commit()

        return result.rowcount
