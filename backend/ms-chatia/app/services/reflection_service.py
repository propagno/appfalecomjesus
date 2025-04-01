import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.study import Reflection
from app.schemas.study import ReflectionCreate

logger = logging.getLogger(__name__)


class ReflectionService:
    """
    Serviço para gerenciamento de reflexões.

    Responsável por:
    - Salvar reflexões pessoais
    - Listar histórico
    - Buscar por tema ou data
    - Gerar insights espirituais

    Attributes:
        db: Sessão do banco de dados
    """

    def __init__(self, db: Session):
        """
        Inicializa o serviço de reflexões.

        Args:
            db: Sessão do banco de dados
        """
        self.db = db

    async def create_reflection(
        self,
        user_id: UUID,
        reflection: ReflectionCreate
    ) -> Dict:
        """
        Salva nova reflexão pessoal.

        Args:
            user_id: ID do usuário
            reflection: Dados da reflexão

        Returns:
            Dict com detalhes salvos

        Raises:
            HTTPException: Se erro ao salvar
        """
        try:
            # Cria reflexão
            new_reflection = Reflection(
                user_id=user_id,
                study_section_id=reflection.study_section_id,
                verse_id=reflection.verse_id,
                chat_message_id=reflection.chat_message_id,
                reflection_text=reflection.reflection_text,
                tags=reflection.tags,
                created_at=datetime.utcnow()
            )

            self.db.add(new_reflection)
            self.db.commit()
            self.db.refresh(new_reflection)

            return {
                "id": new_reflection.id,
                "reflection_text": new_reflection.reflection_text,
                "tags": new_reflection.tags,
                "created_at": new_reflection.created_at
            }

        except Exception as e:
            logger.error(f"Error creating reflection: {str(e)}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao salvar reflexão"
            )

    async def get_reflection(
        self,
        reflection_id: UUID,
        user_id: UUID
    ) -> Optional[Dict]:
        """
        Retorna detalhes da reflexão.

        Args:
            reflection_id: ID da reflexão
            user_id: ID do usuário

        Returns:
            Dict com detalhes ou None

        Raises:
            HTTPException: Se erro na busca
        """
        try:
            reflection = self.db.query(Reflection).filter(
                Reflection.id == reflection_id,
                Reflection.user_id == user_id
            ).first()

            if not reflection:
                return None

            return {
                "id": reflection.id,
                "reflection_text": reflection.reflection_text,
                "study_section_id": reflection.study_section_id,
                "verse_id": reflection.verse_id,
                "chat_message_id": reflection.chat_message_id,
                "tags": reflection.tags,
                "created_at": reflection.created_at
            }

        except Exception as e:
            logger.error(f"Error getting reflection: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao buscar reflexão"
            )

    async def list_reflections(
        self,
        user_id: UUID,
        study_section_id: Optional[UUID] = None,
        verse_id: Optional[UUID] = None,
        chat_message_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 10,
        offset: int = 0
    ) -> List[Dict]:
        """
        Lista reflexões com filtros.

        Args:
            user_id: ID do usuário
            study_section_id: Filtro por seção
            verse_id: Filtro por versículo
            chat_message_id: Filtro por mensagem
            tags: Filtro por tags
            start_date: Data inicial
            end_date: Data final
            limit: Limite de registros
            offset: Deslocamento

        Returns:
            Lista de reflexões

        Raises:
            HTTPException: Se erro na listagem
        """
        try:
            # Query base
            query = self.db.query(Reflection).filter(
                Reflection.user_id == user_id
            )

            # Aplica filtros
            if study_section_id:
                query = query.filter(
                    Reflection.study_section_id == study_section_id)

            if verse_id:
                query = query.filter(Reflection.verse_id == verse_id)

            if chat_message_id:
                query = query.filter(
                    Reflection.chat_message_id == chat_message_id)

            if tags:
                query = query.filter(Reflection.tags.overlap(tags))

            if start_date:
                query = query.filter(Reflection.created_at >= start_date)

            if end_date:
                query = query.filter(Reflection.created_at <= end_date)

            # Ordena e pagina
            reflections = query.order_by(
                Reflection.created_at.desc()
            ).offset(offset).limit(limit).all()

            return [{
                "id": r.id,
                "reflection_text": r.reflection_text,
                "study_section_id": r.study_section_id,
                "verse_id": r.verse_id,
                "chat_message_id": r.chat_message_id,
                "tags": r.tags,
                "created_at": r.created_at
            } for r in reflections]

        except Exception as e:
            logger.error(f"Error listing reflections: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao listar reflexões"
            )

    async def update_reflection(
        self,
        reflection_id: UUID,
        user_id: UUID,
        reflection_text: str,
        tags: Optional[List[str]] = None
    ) -> Dict:
        """
        Atualiza texto da reflexão.

        Args:
            reflection_id: ID da reflexão
            user_id: ID do usuário
            reflection_text: Novo texto
            tags: Novas tags

        Returns:
            Dict com detalhes atualizados

        Raises:
            HTTPException: Se erro na atualização
        """
        try:
            reflection = self.db.query(Reflection).filter(
                Reflection.id == reflection_id,
                Reflection.user_id == user_id
            ).first()

            if not reflection:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Reflexão não encontrada"
                )

            reflection.reflection_text = reflection_text
            if tags is not None:
                reflection.tags = tags

            self.db.commit()
            self.db.refresh(reflection)

            return {
                "id": reflection.id,
                "reflection_text": reflection.reflection_text,
                "tags": reflection.tags,
                "created_at": reflection.created_at
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating reflection: {str(e)}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar reflexão"
            )

    async def delete_reflection(
        self,
        reflection_id: UUID,
        user_id: UUID
    ) -> None:
        """
        Remove reflexão do usuário.

        Args:
            reflection_id: ID da reflexão
            user_id: ID do usuário

        Raises:
            HTTPException: Se erro na remoção
        """
        try:
            reflection = self.db.query(Reflection).filter(
                Reflection.id == reflection_id,
                Reflection.user_id == user_id
            ).first()

            if not reflection:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Reflexão não encontrada"
                )

            self.db.delete(reflection)
            self.db.commit()

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting reflection: {str(e)}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao remover reflexão"
            )

    async def get_reflection_stats(
        self,
        user_id: UUID
    ) -> Dict:
        """
        Retorna estatísticas das reflexões.

        Args:
            user_id: ID do usuário

        Returns:
            Dict com estatísticas

        Raises:
            HTTPException: Se erro no cálculo
        """
        try:
            # Total de reflexões
            total = self.db.query(Reflection).filter(
                Reflection.user_id == user_id
            ).count()

            # Reflexões nos últimos 7 dias
            week_ago = datetime.utcnow() - timedelta(days=7)
            last_week = self.db.query(Reflection).filter(
                Reflection.user_id == user_id,
                Reflection.created_at >= week_ago
            ).count()

            # Tags mais usadas
            tags_query = self.db.query(
                Reflection.tags,
                Reflection.created_at
            ).filter(
                Reflection.user_id == user_id,
                Reflection.tags != None
            ).order_by(
                Reflection.created_at.desc()
            ).limit(100).all()

            tag_count = {}
            for tags, _ in tags_query:
                if tags:
                    for tag in tags:
                        tag_count[tag] = tag_count.get(tag, 0) + 1

            top_tags = sorted(
                tag_count.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]

            return {
                "total_reflections": total,
                "last_week": last_week,
                "top_tags": [{
                    "tag": tag,
                    "count": count
                } for tag, count in top_tags]
            }

        except Exception as e:
            logger.error(f"Error getting stats: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao calcular estatísticas"
            )
