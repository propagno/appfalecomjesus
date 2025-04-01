from typing import List, Tuple, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, desc, asc
from fastapi import HTTPException, status
from uuid import uuid4

from app.models.study_plan import StudyPlan
from app.models.study_section import StudySection
from app.models.study_content import StudyContent
from app.schemas.study_plan import StudyPlanCreate, StudyPlanUpdate, StudyPlanSimple


class StudyPlanService:
    """
    Serviço para operações relacionadas aos planos de estudo.
    """

    def __init__(self, db: Session):
        self.db = db

    async def get_plans(
        self,
        skip: int = 0,
        limit: int = 10,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        search: Optional[str] = None,
        user_id: Optional[str] = None,
        public_only: bool = False,
        sort_by: str = "created_at",
        sort_desc: bool = True
    ) -> Tuple[List[StudyPlanSimple], int]:
        """
        Retorna uma lista paginada de planos de estudo com filtragem.

        Args:
            skip: Quantos planos pular (para paginação)
            limit: Quantos planos retornar por página
            category: Filtrar por categoria
            difficulty: Filtrar por nível de dificuldade
            search: Buscar por título ou descrição
            user_id: ID do usuário para mostrar planos personalizados
            public_only: Se True, mostra apenas planos públicos
            sort_by: Campo para ordenação
            sort_desc: Se True, ordena em ordem decrescente

        Returns:
            Tupla contendo a lista de planos e o total de planos
        """
        # Construir a query base
        query = self.db.query(StudyPlan)

        # Aplicar filtros
        if category:
            query = query.filter(StudyPlan.category == category)

        if difficulty:
            query = query.filter(StudyPlan.difficulty == difficulty)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    StudyPlan.title.ilike(search_term),
                    StudyPlan.description.ilike(search_term)
                )
            )

        # Lógica de visibilidade dos planos
        if public_only:
            query = query.filter(StudyPlan.is_public == True)
        elif user_id:
            # Mostrar planos públicos ou planos do usuário
            query = query.filter(
                or_(
                    StudyPlan.is_public == True,
                    StudyPlan.user_id == user_id
                )
            )
        else:
            # Se não estiver autenticado e não solicitou public_only
            # ainda assim mostrar apenas planos públicos
            query = query.filter(StudyPlan.is_public == True)

        # Contar total antes de aplicar paginação
        total = query.count()

        # Aplicar ordenação
        if sort_by:
            sort_column = getattr(StudyPlan, sort_by, StudyPlan.created_at)
            query = query.order_by(
                desc(sort_column) if sort_desc else asc(sort_column))

        # Aplicar paginação
        query = query.offset(skip).limit(limit)

        # Executar a query
        study_plans = query.all()

        # Converter para objetos StudyPlanSimple e adicionar contagem de seções
        result = []
        for plan in study_plans:
            sections_count = self.db.query(StudySection).filter(
                StudySection.study_plan_id == plan.id
            ).count()

            # Criar objeto StudyPlanSimple
            plan_simple = StudyPlanSimple(
                id=plan.id,
                title=plan.title,
                description=plan.description,
                category=plan.category,
                difficulty=plan.difficulty,
                duration_days=plan.duration_days,
                image_url=plan.image_url,
                created_at=plan.created_at,
                sections_count=sections_count
            )
            result.append(plan_simple)

        return result, total

    async def get_plan_by_id(self, plan_id: str) -> StudyPlan:
        """
        Retorna um plano de estudo pelo ID, incluindo seções e conteúdos.

        Args:
            plan_id: ID do plano de estudo

        Returns:
            Plano de estudo com suas seções e conteúdos ou None se não encontrado
        """
        # Buscar o plano de estudo
        study_plan = self.db.query(StudyPlan).filter(
            StudyPlan.id == plan_id).first()

        if not study_plan:
            return None

        # Carregar seções e conteúdos (alternativa a lazy loading)
        sections = self.db.query(StudySection).filter(
            StudySection.study_plan_id == plan_id
        ).order_by(StudySection.position).all()

        for section in sections:
            contents = self.db.query(StudyContent).filter(
                StudyContent.section_id == section.id
            ).order_by(StudyContent.position).all()
            section.contents = contents

        study_plan.sections = sections

        return study_plan

    async def create_plan(self, plan_data: StudyPlanCreate) -> StudyPlan:
        """
        Cria um novo plano de estudo no banco de dados.

        Args:
            plan_data: Dados do plano a ser criado

        Returns:
            Plano de estudo criado
        """
        # Criar o plano de estudo
        study_plan = StudyPlan(
            id=str(uuid4()),
            title=plan_data.title,
            description=plan_data.description,
            category=plan_data.category,
            difficulty=plan_data.difficulty,
            duration_days=plan_data.duration_days,
            image_url=plan_data.image_url,
            is_public=plan_data.is_public,
            user_id=plan_data.user_id,
            created_by_ia=plan_data.created_by_ia
        )

        self.db.add(study_plan)
        self.db.flush()  # Para obter o ID sem commit

        # Criar seções, se houver
        if plan_data.sections:
            for i, section_data in enumerate(plan_data.sections):
                section = StudySection(
                    id=str(uuid4()),
                    study_plan_id=study_plan.id,
                    title=section_data.title,
                    description=section_data.description,
                    position=section_data.position if section_data.position is not None else i,
                    duration_minutes=section_data.duration_minutes,
                    bible_reference=section_data.bible_reference
                )

                self.db.add(section)
                self.db.flush()

                # Criar conteúdos da seção, se houver
                if section_data.contents:
                    for j, content_data in enumerate(section_data.contents):
                        content = StudyContent(
                            id=str(uuid4()),
                            section_id=section.id,
                            content_type=content_data.content_type,
                            content=content_data.content,
                            position=content_data.position if content_data.position is not None else j,
                            title=content_data.title
                        )

                        self.db.add(content)

        # Salvar as alterações
        self.db.commit()
        self.db.refresh(study_plan)

        # Carregar o plano completo
        return await self.get_plan_by_id(study_plan.id)

    async def update_plan(self, plan_id: str, plan_update: StudyPlanUpdate) -> StudyPlan:
        """
        Atualiza um plano de estudo existente.

        Args:
            plan_id: ID do plano a ser atualizado
            plan_update: Dados atualizados do plano

        Returns:
            Plano de estudo atualizado

        Raises:
            HTTPException: Se o plano não existir
        """
        # Buscar o plano existente
        study_plan = self.db.query(StudyPlan).filter(
            StudyPlan.id == plan_id).first()

        if not study_plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plano de estudo não encontrado"
            )

        # Atualizar campos
        update_data = plan_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(study_plan, key, value)

        # Salvar alterações
        self.db.commit()
        self.db.refresh(study_plan)

        # Carregar o plano completo
        return await self.get_plan_by_id(study_plan.id)

    async def delete_plan(self, plan_id: str) -> None:
        """
        Exclui um plano de estudo e todas suas seções e conteúdos.

        Args:
            plan_id: ID do plano a ser excluído

        Raises:
            HTTPException: Se o plano não existir
        """
        # Buscar o plano existente
        study_plan = self.db.query(StudyPlan).filter(
            StudyPlan.id == plan_id).first()

        if not study_plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plano de estudo não encontrado"
            )

        # Excluir o plano (as seções e conteúdos serão excluídos automaticamente pelo CASCADE)
        self.db.delete(study_plan)
        self.db.commit()

    async def get_recommendations(self, user_id: str, limit: int = 5) -> List[StudyPlanSimple]:
        """
        Obtém recomendações de planos de estudo para o usuário.

        Args:
            user_id: ID do usuário
            limit: Número máximo de recomendações

        Returns:
            Lista de planos de estudo recomendados
        """
        # Esta é uma implementação simplificada de recomendação
        # Em um sistema real, usaria um algoritmo mais sofisticado considerando:
        # - Histórico de estudos completados
        # - Preferências do usuário
        # - Popularidade dos planos
        # - Categorias de interesse

        # Por enquanto, retorna planos públicos populares que o usuário ainda não iniciou
        # Popularidade aqui é simulada pela ordem de criação (mais recentes primeiro)

        query = self.db.query(StudyPlan).filter(
            StudyPlan.is_public == True,
            StudyPlan.user_id != user_id  # Não recomendar planos criados pelo próprio usuário
        ).order_by(desc(StudyPlan.created_at)).limit(limit)

        study_plans = query.all()

        # Converter para objetos StudyPlanSimple e adicionar contagem de seções
        result = []
        for plan in study_plans:
            sections_count = self.db.query(StudySection).filter(
                StudySection.study_plan_id == plan.id
            ).count()

            # Criar objeto StudyPlanSimple
            plan_simple = StudyPlanSimple(
                id=plan.id,
                title=plan.title,
                description=plan.description,
                category=plan.category,
                difficulty=plan.difficulty,
                duration_days=plan.duration_days,
                image_url=plan.image_url,
                created_at=plan.created_at,
                sections_count=sections_count
            )
            result.append(plan_simple)

        return result
