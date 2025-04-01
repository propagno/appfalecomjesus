import uuid
import logging
from typing import Optional, Dict, Any, List, Tuple

from app.models.user_study_progress import UserStudyProgress
from app.models.study_plan import StudyPlan
from app.repositories.user_study_progress_repository import UserStudyProgressRepository
from app.repositories.study_plan_repository import StudyPlanRepository

# Configurar logger
logger = logging.getLogger(__name__)


class StudyProgressService:
    """
    Serviço para gerenciar o progresso de estudo do usuário.
    """

    def __init__(self, progress_repository: UserStudyProgressRepository, study_plan_repository: StudyPlanRepository):
        self.progress_repository = progress_repository
        self.study_plan_repository = study_plan_repository

    async def get_user_progress(self, user_id: uuid.UUID, study_plan_id: uuid.UUID) -> Optional[UserStudyProgress]:
        """
        Obtém o progresso de um usuário em um plano de estudo específico.

        Args:
            user_id: ID do usuário
            study_plan_id: ID do plano de estudo

        Returns:
            Optional[UserStudyProgress]: O progresso do usuário ou None se não existir
        """
        return await self.progress_repository.get_by_user_and_plan(user_id, study_plan_id)

    async def get_all_user_progress(self, user_id: uuid.UUID) -> List[Dict[str, Any]]:
        """
        Obtém o progresso do usuário em todos os planos de estudo.

        Args:
            user_id: ID do usuário

        Returns:
            List[Dict[str, Any]]: Lista de progressos com informações dos planos
        """
        progress_list = await self.progress_repository.get_by_user_id(user_id)

        # Obter detalhes dos planos de estudo
        result = []
        for progress in progress_list:
            plan = await self.study_plan_repository.get_by_id(progress.study_plan_id)
            if plan:
                result.append({
                    "progress": progress,
                    "plan": plan
                })

        return result

    async def update_progress(
        self,
        user_id: uuid.UUID,
        study_plan_id: uuid.UUID,
        section_id: Optional[uuid.UUID],
        completion_percentage: float
    ) -> Tuple[UserStudyProgress, bool]:
        """
        Atualiza o progresso de um usuário em um plano de estudo.

        Args:
            user_id: ID do usuário
            study_plan_id: ID do plano de estudo
            section_id: ID da seção atual (opcional)
            completion_percentage: Percentual de conclusão (0-100)

        Returns:
            Tuple[UserStudyProgress, bool]: O progresso atualizado e um indicador se o plano foi concluído
        """
        # Verificar se o plano existe
        plan = await self.study_plan_repository.get_by_id(study_plan_id)
        if not plan:
            logger.error(f"Plano de estudo não encontrado: {study_plan_id}")
            raise ValueError(
                f"Plano de estudo não encontrado: {study_plan_id}")

        # Verificar se já existe um progresso para este usuário e plano
        existing_progress = await self.get_user_progress(user_id, study_plan_id)

        # Determinar se o plano foi concluído (100%)
        was_completed = False
        is_completed_now = completion_percentage >= 100

        if existing_progress:
            was_completed = existing_progress.completion_percentage >= 100

            # Atualizar o progresso existente
            progress = await self.progress_repository.update(
                existing_progress.id,
                current_section_id=section_id,
                completion_percentage=completion_percentage
            )
        else:
            # Criar um novo progresso
            progress = await self.progress_repository.create(
                user_id=user_id,
                study_plan_id=study_plan_id,
                current_section_id=section_id,
                completion_percentage=completion_percentage
            )

        # Verificar se o plano foi concluído agora
        plan_newly_completed = is_completed_now and not was_completed

        # Registrar a conclusão no log para debug
        if plan_newly_completed:
            logger.info(
                f"Plano concluído pelo usuário: user_id={user_id}, study_plan_id={study_plan_id}")

        # Retornar o progresso e o indicador de conclusão
        return progress, plan_newly_completed

    async def start_plan(self, user_id: uuid.UUID, study_plan_id: uuid.UUID, first_section_id: Optional[uuid.UUID] = None) -> UserStudyProgress:
        """
        Inicia um plano de estudo para o usuário.

        Args:
            user_id: ID do usuário
            study_plan_id: ID do plano de estudo
            first_section_id: ID da primeira seção (opcional)

        Returns:
            UserStudyProgress: O progresso criado
        """
        # Verificar se o plano existe
        plan = await self.study_plan_repository.get_by_id(study_plan_id)
        if not plan:
            logger.error(f"Plano de estudo não encontrado: {study_plan_id}")
            raise ValueError(
                f"Plano de estudo não encontrado: {study_plan_id}")

        # Verificar se já existe um progresso para este usuário e plano
        existing_progress = await self.get_user_progress(user_id, study_plan_id)

        if existing_progress:
            logger.info(
                f"Usuário já iniciou este plano: user_id={user_id}, study_plan_id={study_plan_id}")
            return existing_progress

        # Criar um novo progresso com 0% de conclusão
        progress = await self.progress_repository.create(
            user_id=user_id,
            study_plan_id=study_plan_id,
            current_section_id=first_section_id,
            completion_percentage=0
        )

        logger.info(
            f"Plano iniciado com sucesso: user_id={user_id}, study_plan_id={study_plan_id}")

        return progress

    async def get_completed_plans(self, user_id: uuid.UUID) -> List[Dict[str, Any]]:
        """
        Obtém todos os planos de estudo concluídos pelo usuário.

        Args:
            user_id: ID do usuário

        Returns:
            List[Dict[str, Any]]: Lista de planos concluídos com progresso
        """
        completed_progress = await self.progress_repository.get_completed_by_user(user_id)

        # Obter detalhes dos planos
        result = []
        for progress in completed_progress:
            plan = await self.study_plan_repository.get_by_id(progress.study_plan_id)
            if plan:
                result.append({
                    "progress": progress,
                    "plan": plan
                })

        return result
