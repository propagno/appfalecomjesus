from typing import Dict, List, Optional
import logging
from uuid import UUID
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models.study import StudyPlan, StudySection, StudyContent
from app.schemas.chat import StudyPlanRequest, StudyPlanResponse
from app.services.openai_service import OpenAIService

logger = get_logger(__name__)


class StudyService:
    """
    Serviço responsável por gerenciar planos de estudo personalizados.

    O serviço coordena:
    1. Geração de planos via IA
    2. Persistência no banco de dados
    3. Acompanhamento de progresso
    4. Geração de certificados

    Attributes:
        db: Sessão do banco de dados
        openai: Serviço da OpenAI para geração de conteúdo
    """

    def __init__(self, db: Session):
        """
        Inicializa o serviço com dependências.

        Args:
            db: Sessão do banco de dados
        """
        self.db = db
        self.openai = OpenAIService()

    async def create_study_plan(
        self,
        user_id: UUID,
        preferences: StudyPlanRequest
    ) -> StudyPlanResponse:
        """
        Cria um novo plano de estudo personalizado.

        O fluxo inclui:
        1. Validar preferências
        2. Gerar plano via IA
        3. Persistir no banco
        4. Retornar resposta estruturada

        Args:
            user_id: ID do usuário
            preferences: Preferências para o plano

        Returns:
            StudyPlanResponse com detalhes do plano

        Raises:
            HTTPException: Se erro na geração ou persistência
        """
        try:
            # Gerar plano via IA
            plan_response = await self.openai.generate_study_plan(
                user_id,
                preferences
            )

            # Criar modelo do plano
            study_plan = StudyPlan(
                user_id=user_id,
                title=plan_response.title,
                description=plan_response.description,
                duration_days=plan_response.duration_days,
                daily_duration=plan_response.daily_duration
            )

            # Persistir plano
            self.db.add(study_plan)
            self.db.commit()
            self.db.refresh(study_plan)

            # Criar seções
            for session in plan_response.sessions:
                study_section = StudySection(
                    study_plan_id=study_plan.id,
                    title=session.title,
                    position=session.position,
                    duration_minutes=session.duration
                )
                self.db.add(study_section)

                # Criar conteúdos
                for content in session.contents:
                    study_content = StudyContent(
                        section_id=study_section.id,
                        content_type=content.type,
                        content=content.text,
                        position=content.position
                    )
                    self.db.add(study_content)

            self.db.commit()

            return plan_response

        except Exception as e:
            logger.error(f"Error creating study plan: {str(e)}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar plano de estudo"
            )

    async def get_study_plan(
        self,
        user_id: UUID,
        plan_id: UUID
    ) -> StudyPlanResponse:
        """
        Recupera um plano de estudo específico.

        Args:
            user_id: ID do usuário
            plan_id: ID do plano

        Returns:
            StudyPlanResponse com detalhes do plano

        Raises:
            HTTPException: Se plano não encontrado ou acesso negado
        """
        try:
            # Buscar plano
            plan = self.db.query(StudyPlan).filter(
                StudyPlan.id == plan_id,
                StudyPlan.user_id == user_id
            ).first()

            if not plan:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Plano não encontrado"
                )

            # Buscar seções e conteúdos
            sections = []
            for section in plan.sections:
                contents = []
                for content in section.contents:
                    contents.append({
                        "type": content.content_type,
                        "text": content.content,
                        "position": content.position
                    })

                sections.append({
                    "title": section.title,
                    "position": section.position,
                    "duration": section.duration_minutes,
                    "contents": contents
                })

            return StudyPlanResponse(
                id=plan.id,
                title=plan.title,
                description=plan.description,
                duration_days=plan.duration_days,
                daily_duration=plan.daily_duration,
                sessions=sections
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting study plan: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao recuperar plano"
            )

    async def update_progress(
        self,
        user_id: UUID,
        plan_id: UUID,
        section_id: UUID,
        completed: bool
    ) -> Dict:
        """
        Atualiza o progresso em uma seção do plano.

        Args:
            user_id: ID do usuário
            plan_id: ID do plano
            section_id: ID da seção
            completed: Se a seção foi concluída

        Returns:
            Dict com status atualizado

        Raises:
            HTTPException: Se erro na atualização
        """
        try:
            # Validar acesso
            plan = self.db.query(StudyPlan).filter(
                StudyPlan.id == plan_id,
                StudyPlan.user_id == user_id
            ).first()

            if not plan:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Plano não encontrado"
                )

            # Atualizar seção
            section = self.db.query(StudySection).filter(
                StudySection.id == section_id,
                StudySection.study_plan_id == plan_id
            ).first()

            if not section:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Seção não encontrada"
                )

            section.completed = completed
            section.completed_at = datetime.utcnow() if completed else None

            self.db.commit()

            # Calcular progresso
            total_sections = len(plan.sections)
            completed_sections = len([
                s for s in plan.sections if s.completed
            ])

            progress = (completed_sections / total_sections) * 100

            return {
                "completed": completed,
                "progress": progress,
                "total_sections": total_sections,
                "completed_sections": completed_sections
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating progress: {str(e)}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar progresso"
            )

    async def generate_certificate(
        self,
        user_id: UUID,
        plan_id: UUID
    ) -> Dict:
        """
        Gera certificado de conclusão do plano.

        Args:
            user_id: ID do usuário
            plan_id: ID do plano

        Returns:
            Dict com dados do certificado

        Raises:
            HTTPException: Se plano não concluído ou erro na geração
        """
        try:
            # Validar conclusão
            plan = self.db.query(StudyPlan).filter(
                StudyPlan.id == plan_id,
                StudyPlan.user_id == user_id
            ).first()

            if not plan:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Plano não encontrado"
                )

            completed_sections = len([
                s for s in plan.sections if s.completed
            ])

            if completed_sections < len(plan.sections):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Plano não concluído totalmente"
                )

            # Gerar certificado
            certificate_data = {
                "user_id": user_id,
                "plan_id": plan_id,
                "plan_title": plan.title,
                "completion_date": datetime.utcnow(),
                "certificate_code": f"CERT-{plan_id}"
            }

            # TODO: Implementar geração do PDF

            return certificate_data

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error generating certificate: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao gerar certificado"
            )
