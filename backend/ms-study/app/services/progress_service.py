from typing import List, Tuple, Optional, Dict
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc
from fastapi import HTTPException, status
from uuid import uuid4

from app.models.user_study_progress import UserStudyProgress
from app.models.study_plan import StudyPlan
from app.models.study_section import StudySection
from app.schemas.progress import UserStudyProgressCreate, UserStudyProgressUpdate, UserStudyProgressDetail


class ProgressService:
    """
    Serviço para operações relacionadas ao progresso do usuário nos planos de estudo.
    """

    def __init__(self, db: Session):
        self.db = db

    async def get_user_progress_list(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 10,
        completed: Optional[bool] = None,
        sort_by: str = "last_activity_date",
        sort_desc: bool = True
    ) -> Tuple[List[UserStudyProgressDetail], int]:
        """
        Retorna uma lista paginada de progresso do usuário em planos de estudo.

        Args:
            user_id: ID do usuário
            skip: Quantos itens pular (para paginação)
            limit: Quantos itens retornar por página
            completed: Se True, apenas planos concluídos; se False, apenas não concluídos; se None, todos
            sort_by: Campo para ordenação
            sort_desc: Se True, ordena em ordem decrescente

        Returns:
            Tupla contendo a lista de progressos com detalhes e o total de progressos
        """
        # Construir a query base
        query = self.db.query(UserStudyProgress).filter(
            UserStudyProgress.user_id == user_id)

        # Aplicar filtro de conclusão se especificado
        if completed is not None:
            if completed:
                query = query.filter(
                    UserStudyProgress.completed_at.isnot(None))
            else:
                query = query.filter(UserStudyProgress.completed_at.is_(None))

        # Contar total antes de aplicar paginação
        total = query.count()

        # Aplicar ordenação
        if sort_by:
            sort_column = getattr(UserStudyProgress, sort_by,
                                  UserStudyProgress.last_activity_date)
            query = query.order_by(
                desc(sort_column) if sort_desc else asc(sort_column))

        # Aplicar paginação
        query = query.offset(skip).limit(limit)

        # Executar a query
        progress_list = query.all()

        # Converter para objetos UserStudyProgressDetail com informações adicionais
        result = []
        for progress in progress_list:
            # Buscar o plano associado
            plan = self.db.query(StudyPlan).filter(
                StudyPlan.id == progress.study_plan_id).first()

            # Buscar a seção atual, se houver
            current_section = None
            current_section_title = None
            current_section_position = None
            if progress.current_section_id:
                current_section = self.db.query(StudySection).filter(
                    StudySection.id == progress.current_section_id
                ).first()
                if current_section:
                    current_section_title = current_section.title
                    current_section_position = current_section.position

            # Contar total de seções
            total_sections = self.db.query(StudySection).filter(
                StudySection.study_plan_id == progress.study_plan_id
            ).count()

            # Criar objeto UserStudyProgressDetail
            progress_detail = UserStudyProgressDetail(
                id=progress.id,
                user_id=progress.user_id,
                study_plan_id=progress.study_plan_id,
                current_section_id=progress.current_section_id,
                completion_percentage=progress.completion_percentage,
                last_activity_date=progress.last_activity_date,
                started_at=progress.started_at,
                completed_at=progress.completed_at,
                created_at=progress.created_at,
                updated_at=progress.updated_at,
                # Adicionar informações do plano
                plan_title=plan.title if plan else "Plano indisponível",
                plan_description=plan.description if plan else None,
                plan_duration_days=plan.duration_days if plan else 0,
                plan_category=plan.category if plan else None,
                plan_difficulty=plan.difficulty if plan else None,
                # Adicionar informações da seção atual
                current_section_title=current_section_title,
                current_section_position=current_section_position,
                total_sections=total_sections
            )
            result.append(progress_detail)

        return result, total

    async def get_progress_by_id(self, progress_id: str) -> Optional[UserStudyProgress]:
        """
        Retorna o progresso pelo ID.

        Args:
            progress_id: ID do progresso

        Returns:
            Objeto UserStudyProgress ou None se não encontrado
        """
        return self.db.query(UserStudyProgress).filter(UserStudyProgress.id == progress_id).first()

    async def get_progress_detail(self, progress_id: str) -> Optional[UserStudyProgressDetail]:
        """
        Retorna detalhes do progresso, incluindo informações do plano e seção atual.

        Args:
            progress_id: ID do progresso

        Returns:
            Objeto UserStudyProgressDetail ou None se não encontrado
        """
        # Buscar o progresso
        progress = await self.get_progress_by_id(progress_id)
        if not progress:
            return None

        # Buscar o plano associado
        plan = self.db.query(StudyPlan).filter(
            StudyPlan.id == progress.study_plan_id).first()

        # Buscar a seção atual, se houver
        current_section = None
        current_section_title = None
        current_section_position = None
        if progress.current_section_id:
            current_section = self.db.query(StudySection).filter(
                StudySection.id == progress.current_section_id
            ).first()
            if current_section:
                current_section_title = current_section.title
                current_section_position = current_section.position

        # Contar total de seções
        total_sections = self.db.query(StudySection).filter(
            StudySection.study_plan_id == progress.study_plan_id
        ).count()

        # Criar objeto UserStudyProgressDetail
        return UserStudyProgressDetail(
            id=progress.id,
            user_id=progress.user_id,
            study_plan_id=progress.study_plan_id,
            current_section_id=progress.current_section_id,
            completion_percentage=progress.completion_percentage,
            last_activity_date=progress.last_activity_date,
            started_at=progress.started_at,
            completed_at=progress.completed_at,
            created_at=progress.created_at,
            updated_at=progress.updated_at,
            # Adicionar informações do plano
            plan_title=plan.title if plan else "Plano indisponível",
            plan_description=plan.description if plan else None,
            plan_duration_days=plan.duration_days if plan else 0,
            plan_category=plan.category if plan else None,
            plan_difficulty=plan.difficulty if plan else None,
            # Adicionar informações da seção atual
            current_section_title=current_section_title,
            current_section_position=current_section_position,
            total_sections=total_sections
        )

    async def get_progress_by_plan(self, user_id: str, plan_id: str) -> Optional[UserStudyProgressDetail]:
        """
        Retorna o progresso de um usuário em um plano específico.

        Args:
            user_id: ID do usuário
            plan_id: ID do plano de estudo

        Returns:
            Objeto UserStudyProgressDetail ou None se não encontrado
        """
        # Buscar o progresso
        progress = self.db.query(UserStudyProgress).filter(
            UserStudyProgress.user_id == user_id,
            UserStudyProgress.study_plan_id == plan_id
        ).first()

        if not progress:
            return None

        # Converter para detalhes completos
        return await self.get_progress_detail(progress.id)

    async def start_study_plan(self, progress_data: UserStudyProgressCreate) -> UserStudyProgress:
        """
        Inicia um novo plano de estudo para o usuário ou retorna o existente.

        Args:
            progress_data: Dados do progresso a ser criado

        Returns:
            Objeto UserStudyProgress criado ou existente

        Raises:
            HTTPException: Se o plano não existir
        """
        # Verificar se o plano existe
        plan = self.db.query(StudyPlan).filter(
            StudyPlan.id == progress_data.study_plan_id).first()
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plano de estudo não encontrado"
            )

        # Verificar se o usuário já iniciou este plano
        existing_progress = self.db.query(UserStudyProgress).filter(
            UserStudyProgress.user_id == progress_data.user_id,
            UserStudyProgress.study_plan_id == progress_data.study_plan_id
        ).first()

        if existing_progress:
            # Se já existe, atualizar a data de última atividade
            existing_progress.last_activity_date = datetime.utcnow()
            self.db.commit()
            self.db.refresh(existing_progress)
            return existing_progress

        # Buscar a primeira seção do plano
        first_section = self.db.query(StudySection).filter(
            StudySection.study_plan_id == progress_data.study_plan_id
        ).order_by(StudySection.position).first()

        # Criar novo progresso
        progress = UserStudyProgress(
            id=str(uuid4()),
            user_id=progress_data.user_id,
            study_plan_id=progress_data.study_plan_id,
            current_section_id=first_section.id if first_section else None,
            # Se não há seções, considerar 100%
            completion_percentage=0.0 if first_section else 100.0,
            last_activity_date=datetime.utcnow(),
            started_at=datetime.utcnow()
        )

        self.db.add(progress)
        self.db.commit()
        self.db.refresh(progress)

        return progress

    async def update_progress(self, progress_id: str, progress_update: UserStudyProgressUpdate) -> UserStudyProgressDetail:
        """
        Atualiza o progresso do usuário em um plano de estudo.

        Args:
            progress_id: ID do progresso a atualizar
            progress_update: Dados atualizados do progresso

        Returns:
            Objeto UserStudyProgressDetail atualizado

        Raises:
            HTTPException: Se o progresso não existir
        """
        # Buscar o progresso existente
        progress = self.db.query(UserStudyProgress).filter(
            UserStudyProgress.id == progress_id).first()

        if not progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Progresso não encontrado"
            )

        # Atualizar campos permitidos
        update_data = progress_update.dict(exclude_unset=True)

        # Se estiver atualizando a seção atual, verificar se ela existe e pertence ao plano
        if "current_section_id" in update_data and update_data["current_section_id"]:
            section = self.db.query(StudySection).filter(
                StudySection.id == update_data["current_section_id"],
                StudySection.study_plan_id == progress.study_plan_id
            ).first()

            if not section:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Seção inválida para este plano de estudo"
                )

        # Se estiver marcando como concluído e completed_at não foi definido
        if "completion_percentage" in update_data and update_data["completion_percentage"] >= 100.0:
            if "completed_at" not in update_data or not update_data["completed_at"]:
                update_data["completed_at"] = datetime.utcnow()

        # Atualizar a data de última atividade
        update_data["last_activity_date"] = datetime.utcnow()

        # Aplicar atualizações
        for key, value in update_data.items():
            setattr(progress, key, value)

        self.db.commit()
        self.db.refresh(progress)

        # Retornar os detalhes completos
        return await self.get_progress_detail(progress.id)

    async def complete_section(self, user_id: str, plan_id: str) -> UserStudyProgressDetail:
        """
        Marca a seção atual como concluída e avança para a próxima seção do plano.

        Args:
            user_id: ID do usuário
            plan_id: ID do plano de estudo

        Returns:
            Objeto UserStudyProgressDetail atualizado

        Raises:
            ValueError: Se não houver progresso para o plano ou se já estiver concluído
        """
        # Buscar o progresso existente
        progress = self.db.query(UserStudyProgress).filter(
            UserStudyProgress.user_id == user_id,
            UserStudyProgress.study_plan_id == plan_id
        ).first()

        if not progress:
            raise ValueError(
                "Progresso não encontrado para este plano de estudo")

        if progress.completed_at:
            raise ValueError("Este plano de estudo já foi concluído")

        # Buscar a seção atual
        current_section = None
        if progress.current_section_id:
            current_section = self.db.query(StudySection).filter(
                StudySection.id == progress.current_section_id
            ).first()

        if not current_section:
            raise ValueError("Não há seção atual para este progresso")

        # Buscar todas as seções do plano ordenadas por posição
        sections = self.db.query(StudySection).filter(
            StudySection.study_plan_id == plan_id
        ).order_by(StudySection.position).all()

        # Contar total de seções
        total_sections = len(sections)

        if total_sections == 0:
            raise ValueError("Este plano não possui seções")

        # Encontrar a posição atual e a próxima seção
        current_position = -1
        for i, section in enumerate(sections):
            if section.id == current_section.id:
                current_position = i
                break

        # Se a seção atual não foi encontrada (não deveria acontecer)
        if current_position == -1:
            raise ValueError("Seção atual inválida")

        # Calcular a conclusão atual
        section_weight = 100.0 / total_sections
        current_completion = section_weight * (current_position + 1)

        # Se já estiver na última seção, marcar como concluído
        if current_position == total_sections - 1:
            progress.completion_percentage = 100.0
            # Opcional: remover a seção atual quando concluído
            progress.current_section_id = None
            progress.completed_at = datetime.utcnow()
        else:
            # Avançar para a próxima seção
            next_section = sections[current_position + 1]
            progress.current_section_id = next_section.id
            progress.completion_percentage = current_completion

        # Atualizar data de última atividade
        progress.last_activity_date = datetime.utcnow()

        # Salvar alterações
        self.db.commit()
        self.db.refresh(progress)

        # Retornar os detalhes completos
        return await self.get_progress_detail(progress.id)

    async def reset_progress(self, progress_id: str) -> None:
        """
        Reseta o progresso do usuário em um plano de estudo.

        Args:
            progress_id: ID do progresso a resetar

        Raises:
            HTTPException: Se o progresso não existir
        """
        # Buscar o progresso existente
        progress = self.db.query(UserStudyProgress).filter(
            UserStudyProgress.id == progress_id).first()

        if not progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Progresso não encontrado"
            )

        # Buscar a primeira seção do plano
        first_section = self.db.query(StudySection).filter(
            StudySection.study_plan_id == progress.study_plan_id
        ).order_by(StudySection.position).first()

        # Resetar o progresso
        progress.current_section_id = first_section.id if first_section else None
        progress.completion_percentage = 0.0
        progress.completed_at = None
        progress.last_activity_date = datetime.utcnow()

        # Salvar alterações
        self.db.commit()

    async def get_active_study(self, user_id: str) -> Optional[UserStudyProgressDetail]:
        """
        Retorna o estudo ativo mais recente do usuário.

        Args:
            user_id: ID do usuário

        Returns:
            Objeto UserStudyProgressDetail ou None se não houver estudo ativo
        """
        # Buscar o progresso não concluído mais recente
        progress = self.db.query(UserStudyProgress).filter(
            UserStudyProgress.user_id == user_id,
            UserStudyProgress.completed_at.is_(None)
        ).order_by(desc(UserStudyProgress.last_activity_date)).first()

        if not progress:
            return None

        # Retornar os detalhes completos
        return await self.get_progress_detail(progress.id)
