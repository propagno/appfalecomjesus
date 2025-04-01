from typing import Tuple, List, Optional
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import desc, asc

from app.models.reflection import Reflection
from app.schemas.progress import ReflectionCreate, ReflectionUpdate, ReflectionInDB, ReflectionDetail


class ReflectionService:
    """Serviço para gerenciamento de reflexões pessoais dos usuários"""

    def __init__(self, db: Session):
        self.db = db

    async def get_user_reflections(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 10,
        section_id: Optional[str] = None,
        plan_id: Optional[str] = None,
        sort_by: str = "created_at",
        sort_desc: bool = True
    ) -> Tuple[List[ReflectionDetail], int]:
        """
        Retorna as reflexões do usuário com filtros e paginação.

        Args:
            user_id: ID do usuário
            skip: Itens para pular (paginação)
            limit: Máximo de itens para retornar
            section_id: Filtrar por seção específica
            plan_id: Filtrar por plano de estudo específico
            sort_by: Campo para ordenação
            sort_desc: Se True, ordenação decrescente; se False, crescente

        Returns:
            Tupla com a lista de reflexões e o total de reflexões
        """
        # Construir query base
        query = select(Reflection).where(Reflection.user_id == user_id)

        # Adicionar filtros
        if section_id:
            query = query.where(Reflection.section_id == section_id)

        if plan_id:
            query = query.where(Reflection.plan_id == plan_id)

        # Contar total para paginação
        count_query = select(Reflection).where(Reflection.user_id == user_id)
        if section_id:
            count_query = count_query.where(
                Reflection.section_id == section_id)
        if plan_id:
            count_query = count_query.where(Reflection.plan_id == plan_id)

        result = await self.db.execute(count_query)
        total = len(result.scalars().all())

        # Ordenar resultados
        if hasattr(Reflection, sort_by):
            order_column = getattr(Reflection, sort_by)
            if sort_desc:
                query = query.order_by(desc(order_column))
            else:
                query = query.order_by(asc(order_column))
        else:
            # Ordenação padrão se o campo não existir
            query = query.order_by(desc(Reflection.created_at))

        # Aplicar paginação
        query = query.offset(skip).limit(limit)

        # Executar a consulta
        result = await self.db.execute(query)
        reflections = result.scalars().all()

        # Converter para o schema
        reflection_details = [
            ReflectionDetail(
                id=reflection.id,
                user_id=reflection.user_id,
                section_id=reflection.section_id,
                plan_id=reflection.plan_id,
                reflection_text=reflection.reflection_text,
                created_at=reflection.created_at,
                updated_at=reflection.updated_at,
                section_title=reflection.section_title,
                plan_title=reflection.plan_title
            ) for reflection in reflections
        ]

        return reflection_details, total

    async def create_reflection(self, data: ReflectionCreate) -> ReflectionDetail:
        """
        Cria uma nova reflexão para o usuário.

        Args:
            data: Dados da reflexão a ser criada

        Returns:
            Reflexão criada
        """
        # Verificar se já existe uma reflexão para esta seção e usuário
        existing_query = select(Reflection).where(
            (Reflection.user_id == data.user_id) &
            (Reflection.section_id == data.section_id)
        )
        result = await self.db.execute(existing_query)
        existing = result.scalars().first()

        if existing:
            # Atualizar a existente
            existing.reflection_text = data.reflection_text
            existing.updated_at = datetime.utcnow()
            await self.db.commit()
            await self.db.refresh(existing)
            return ReflectionDetail(
                id=existing.id,
                user_id=existing.user_id,
                section_id=existing.section_id,
                plan_id=existing.plan_id,
                reflection_text=existing.reflection_text,
                created_at=existing.created_at,
                updated_at=existing.updated_at,
                section_title=existing.section_title,
                plan_title=existing.plan_title
            )

        # Criar nova reflexão
        new_reflection = Reflection(
            id=str(uuid4()),
            user_id=data.user_id,
            section_id=data.section_id,
            plan_id=data.plan_id,
            reflection_text=data.reflection_text,
            section_title=data.section_title,
            plan_title=data.plan_title,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.db.add(new_reflection)
        await self.db.commit()
        await self.db.refresh(new_reflection)

        return ReflectionDetail(
            id=new_reflection.id,
            user_id=new_reflection.user_id,
            section_id=new_reflection.section_id,
            plan_id=new_reflection.plan_id,
            reflection_text=new_reflection.reflection_text,
            created_at=new_reflection.created_at,
            updated_at=new_reflection.updated_at,
            section_title=new_reflection.section_title,
            plan_title=new_reflection.plan_title
        )

    async def get_reflection_by_id(self, reflection_id: str) -> Optional[Reflection]:
        """
        Retorna uma reflexão pelo ID.

        Args:
            reflection_id: ID da reflexão

        Returns:
            Reflexão encontrada ou None
        """
        query = select(Reflection).where(Reflection.id == reflection_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_reflection_detail(self, reflection_id: str) -> Optional[ReflectionDetail]:
        """
        Retorna os detalhes de uma reflexão pelo ID.

        Args:
            reflection_id: ID da reflexão

        Returns:
            Detalhes da reflexão ou None
        """
        reflection = await self.get_reflection_by_id(reflection_id)
        if not reflection:
            return None

        return ReflectionDetail(
            id=reflection.id,
            user_id=reflection.user_id,
            section_id=reflection.section_id,
            plan_id=reflection.plan_id,
            reflection_text=reflection.reflection_text,
            created_at=reflection.created_at,
            updated_at=reflection.updated_at,
            section_title=reflection.section_title,
            plan_title=reflection.plan_title
        )

    async def update_reflection(self, reflection_id: str, data: ReflectionUpdate) -> ReflectionDetail:
        """
        Atualiza uma reflexão existente.

        Args:
            reflection_id: ID da reflexão
            data: Novos dados da reflexão

        Returns:
            Reflexão atualizada
        """
        reflection = await self.get_reflection_by_id(reflection_id)

        if not reflection:
            return None

        # Atualizar campos
        reflection.reflection_text = data.reflection_text
        reflection.updated_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(reflection)

        return ReflectionDetail(
            id=reflection.id,
            user_id=reflection.user_id,
            section_id=reflection.section_id,
            plan_id=reflection.plan_id,
            reflection_text=reflection.reflection_text,
            created_at=reflection.created_at,
            updated_at=reflection.updated_at,
            section_title=reflection.section_title,
            plan_title=reflection.plan_title
        )

    async def delete_reflection(self, reflection_id: str) -> bool:
        """
        Exclui uma reflexão pelo ID.

        Args:
            reflection_id: ID da reflexão

        Returns:
            True se excluída com sucesso, False caso contrário
        """
        reflection = await self.get_reflection_by_id(reflection_id)

        if not reflection:
            return False

        await self.db.delete(reflection)
        await self.db.commit()

        return True

    async def get_reflection_by_section(self, user_id: str, section_id: str) -> Optional[ReflectionDetail]:
        """
        Retorna a reflexão de um usuário para uma seção específica.

        Args:
            user_id: ID do usuário
            section_id: ID da seção

        Returns:
            Reflexão do usuário para a seção ou None
        """
        query = select(Reflection).where(
            (Reflection.user_id == user_id) &
            (Reflection.section_id == section_id)
        )

        result = await self.db.execute(query)
        reflection = result.scalars().first()

        if not reflection:
            return None

        return ReflectionDetail(
            id=reflection.id,
            user_id=reflection.user_id,
            section_id=reflection.section_id,
            plan_id=reflection.plan_id,
            reflection_text=reflection.reflection_text,
            created_at=reflection.created_at,
            updated_at=reflection.updated_at,
            section_title=reflection.section_title,
            plan_title=reflection.plan_title
        )

    async def get_recent_reflections(self, user_id: str, limit: int = 5) -> List[ReflectionDetail]:
        """
        Retorna as reflexões mais recentes do usuário.

        Args:
            user_id: ID do usuário
            limit: Número máximo de reflexões para retornar

        Returns:
            Lista das reflexões mais recentes
        """
        query = select(Reflection).where(Reflection.user_id == user_id).order_by(
            desc(Reflection.created_at)
        ).limit(limit)

        result = await self.db.execute(query)
        reflections = result.scalars().all()

        return [
            ReflectionDetail(
                id=reflection.id,
                user_id=reflection.user_id,
                section_id=reflection.section_id,
                plan_id=reflection.plan_id,
                reflection_text=reflection.reflection_text,
                created_at=reflection.created_at,
                updated_at=reflection.updated_at,
                section_title=reflection.section_title,
                plan_title=reflection.plan_title
            ) for reflection in reflections
        ]
