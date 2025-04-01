from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
import logging

from app.models.user_study_progress import UserStudyProgress
from app.schemas.user_study_progress import UserStudyProgressCreate, UserStudyProgressUpdate

logger = logging.getLogger(__name__)


class UserStudyProgressRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, progress_create: UserStudyProgressCreate) -> UserStudyProgress:
        """
        Cria um novo registro de progresso de estudo do usuário.

        Args:
            progress_create: Dados para criação do progresso

        Returns:
            O registro de progresso criado
        """
        progress = UserStudyProgress(**progress_create.dict())
        self.db.add(progress)
        await self.db.commit()
        await self.db.refresh(progress)
        return progress

    async def get_by_id(self, progress_id: str) -> Optional[UserStudyProgress]:
        """
        Obtém um registro de progresso pelo ID.

        Args:
            progress_id: ID do registro de progresso

        Returns:
            O registro de progresso ou None se não for encontrado
        """
        result = await self.db.execute(
            select(UserStudyProgress).where(
                UserStudyProgress.id == progress_id)
        )
        return result.scalars().first()

    async def get_by_user_id(self, user_id: str) -> List[UserStudyProgress]:
        """
        Obtém todos os registros de progresso de um usuário.

        Args:
            user_id: ID do usuário

        Returns:
            Lista de registros de progresso do usuário
        """
        result = await self.db.execute(
            select(UserStudyProgress).where(
                UserStudyProgress.user_id == user_id)
        )
        return result.scalars().all()

    async def get_by_user_and_plan(self, user_id: str, plan_id: str) -> Optional[UserStudyProgress]:
        """
        Obtém o registro de progresso de um usuário em um plano específico.

        Args:
            user_id: ID do usuário
            plan_id: ID do plano de estudo

        Returns:
            O registro de progresso ou None se não for encontrado
        """
        result = await self.db.execute(
            select(UserStudyProgress)
            .where(UserStudyProgress.user_id == user_id)
            .where(UserStudyProgress.study_plan_id == plan_id)
        )
        return result.scalars().first()

    async def update(self, progress_id: str, progress_update: UserStudyProgressUpdate) -> Optional[UserStudyProgress]:
        """
        Atualiza um registro de progresso.

        Args:
            progress_id: ID do registro de progresso
            progress_update: Dados para atualização

        Returns:
            O registro de progresso atualizado ou None se não for encontrado
        """
        update_data = progress_update.dict(exclude_unset=True)

        await self.db.execute(
            update(UserStudyProgress)
            .where(UserStudyProgress.id == progress_id)
            .values(**update_data)
        )
        await self.db.commit()

        return await self.get_by_id(progress_id)

    async def update_by_user_and_plan(
        self, user_id: str, plan_id: str, progress_update: UserStudyProgressUpdate
    ) -> Optional[UserStudyProgress]:
        """
        Atualiza o progresso de um usuário em um plano específico.

        Args:
            user_id: ID do usuário
            plan_id: ID do plano de estudo
            progress_update: Dados para atualização

        Returns:
            O registro de progresso atualizado ou None se não for encontrado
        """
        progress = await self.get_by_user_and_plan(user_id, plan_id)
        if not progress:
            return None

        update_data = progress_update.dict(exclude_unset=True)

        await self.db.execute(
            update(UserStudyProgress)
            .where(UserStudyProgress.id == progress.id)
            .values(**update_data)
        )
        await self.db.commit()

        return await self.get_by_id(progress.id)

    async def delete(self, progress_id: str) -> bool:
        """
        Exclui um registro de progresso.

        Args:
            progress_id: ID do registro de progresso

        Returns:
            True se o registro foi excluído, False caso contrário
        """
        result = await self.db.execute(
            delete(UserStudyProgress).where(
                UserStudyProgress.id == progress_id)
        )
        await self.db.commit()

        return result.rowcount > 0

    async def delete_by_user_id(self, user_id: str) -> int:
        """
        Exclui todos os registros de progresso de um usuário.

        Args:
            user_id: ID do usuário

        Returns:
            Número de registros excluídos
        """
        result = await self.db.execute(
            delete(UserStudyProgress).where(
                UserStudyProgress.user_id == user_id)
        )
        await self.db.commit()

        return result.rowcount
