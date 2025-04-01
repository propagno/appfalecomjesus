from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import httpx
import json
import logging
import uuid
import asyncio

from app.core.config import get_settings
from app.domain.study.models import StudyPlan, StudySection, StudyContent, UserStudyProgress, UserReflection, UserPreferences
from app.domain.study.schemas import (
    UserPreferences as UserPreferencesSchema,
    UserPreferencesResponse,
    StudyPlanCreate, StudyPlanResponse,
    StudySectionCreate, StudySectionResponse,
    StudyContentCreate, StudyContentResponse,
    UserStudyProgressCreate, UserStudyProgressResponse,
    UserReflectionCreate, UserReflectionResponse,
    DailyDevotionalResponse
)

settings = get_settings()
logger = logging.getLogger("study_service")


class StudyService:
    def __init__(self, db: Session):
        self.db = db

    # User Preferences methods
    def create_or_update_user_preferences(self, preferences: UserPreferencesSchema) -> UserPreferencesResponse:
        """
        Cria ou atualiza as preferências de um usuário no banco de dados
        """
        # Verificar se já existem preferências para este usuário
        db_preferences = self.db.query(UserPreferences).filter(
            UserPreferences.user_id == preferences.user_id
        ).first()

        if db_preferences:
            # Atualizar preferências existentes
            db_preferences.objectives = preferences.objectives
            db_preferences.bible_experience_level = preferences.bible_experience_level
            db_preferences.content_preferences = preferences.content_preferences
            db_preferences.preferred_time = preferences.preferred_time
            db_preferences.onboarding_completed = preferences.onboarding_completed
            db_preferences.updated_at = datetime.now()
        else:
            # Criar novas preferências
            db_preferences = UserPreferences(
                id=str(uuid.uuid4()),
                user_id=preferences.user_id,
                objectives=preferences.objectives,
                bible_experience_level=preferences.bible_experience_level,
                content_preferences=preferences.content_preferences,
                preferred_time=preferences.preferred_time,
                onboarding_completed=preferences.onboarding_completed
            )
            self.db.add(db_preferences)

        self.db.commit()
        self.db.refresh(db_preferences)
        return db_preferences

    def get_user_preferences(self, user_id: str) -> Optional[UserPreferencesResponse]:
        """
        Busca as preferências de um usuário pelo ID
        """
        db_preferences = self.db.query(UserPreferences).filter(
            UserPreferences.user_id == user_id
        ).first()
        return db_preferences

    def set_onboarding_completed(self, user_id: str, completed: bool = True) -> Optional[UserPreferencesResponse]:
        """
        Marca o processo de onboarding como concluído para um usuário
        """
        db_preferences = self.db.query(UserPreferences).filter(
            UserPreferences.user_id == user_id
        ).first()

        if not db_preferences:
            return None

        db_preferences.onboarding_completed = completed
        db_preferences.updated_at = datetime.now()
        self.db.commit()
        self.db.refresh(db_preferences)
        return db_preferences

    def update_user_preferences_status(self, user_id: str, has_study_plan: bool = True) -> Optional[UserPreferencesResponse]:
        """
        Atualiza o status das preferências do usuário, indicando se ele já tem um plano de estudo gerado.
        Este método é usado principalmente após a geração bem-sucedida de um plano personalizado.
        """
        db_preferences = self.db.query(UserPreferences).filter(
            UserPreferences.user_id == user_id
        ).first()

        if not db_preferences:
            logger.warning(
                f"Tentativa de atualizar status para usuário {user_id} sem preferências registradas")
            return None

        # Atualiza os campos de status
        db_preferences.has_study_plan = has_study_plan
        db_preferences.updated_at = datetime.now()

        # Se tem um plano, também marca onboarding como concluído por segurança
        if has_study_plan:
            db_preferences.onboarding_completed = True

        self.db.commit()
        self.db.refresh(db_preferences)
        logger.info(
            f"Preferências atualizadas para usuário {user_id}: has_study_plan={has_study_plan}")
        return db_preferences

    # Study Plan methods
    async def generate_study_plan(self, preferences: UserPreferencesSchema) -> Optional[StudyPlanResponse]:
        """
        Gera um plano de estudo personalizado com base nas preferências do usuário
        usando a integração com o MS-ChatIA
        """
        try:
            logger.info(
                f"Iniciando geração de plano para usuário {preferences.user_id}")

            # Salvar as preferências do usuário antes de gerar o plano
            self.create_or_update_user_preferences(preferences)

            # Enviar as preferências para o MS-ChatIA para gerar o plano personalizado
            try:
                async with httpx.AsyncClient(timeout=45.0) as client:
                    response = await client.post(
                        f"{settings.MS_CHATIA_URL}/api/v1/chat/generate-study-plan",
                        json={
                            "user_id": preferences.user_id,
                            "name": preferences.name,
                            "email": preferences.email,
                            "objectives": preferences.objectives,
                            "bible_experience_level": preferences.bible_experience_level,
                            "content_preferences": preferences.content_preferences,
                            "preferred_time": preferences.preferred_time
                        },
                        headers={
                            "Authorization": f"Bearer {settings.SERVICE_API_KEY}"
                        }
                    )

                    if response.status_code != 200:
                        logger.error(
                            f"Erro ao chamar MS-ChatIA: {response.status_code}")
                        logger.error(f"Resposta: {response.text}")
                        return None

                    result = response.json()
                    plan_data = result.get("plan")

                    if not plan_data:
                        logger.error("Plano não encontrado na resposta")
                        return None

                    # Processar o plano e salvar no banco de dados
                    return self._create_plan_from_data(plan_data, preferences.user_id)

            except httpx.RequestError as e:
                logger.error(f"Erro de requisição para MS-ChatIA: {str(e)}")
                return None

        except Exception as e:
            logger.error(f"Erro ao gerar plano de estudo: {str(e)}")
            return None

    def _create_plan_from_data(self, plan_data: dict, user_id: str) -> StudyPlanResponse:
        """
        Cria um plano de estudo no banco de dados a partir dos dados gerados pela IA
        """
        # Criar o plano de estudo
        plan = StudyPlan(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=plan_data.get("title", "Plano de Estudo Personalizado"),
            description=plan_data.get(
                "description", "Plano gerado com base nas suas preferências"),
            duration_days=len(plan_data.get("sections", []))
        )
        self.db.add(plan)
        self.db.flush()

        # Criar as seções e conteúdos
        sections_data = plan_data.get("sections", [])
        for idx, section_data in enumerate(sections_data):
            # Criar a seção
            section = StudySection(
                id=str(uuid.uuid4()),
                study_plan_id=plan.id,
                title=section_data.get("title", f"Dia {idx+1}"),
                position=idx + 1,
                duration_minutes=section_data.get("duration_minutes", 20)
            )
            self.db.add(section)
            self.db.flush()

            # Criar os conteúdos da seção
            contents_data = section_data.get("contents", [])
            for content_idx, content_data in enumerate(contents_data):
                content = StudyContent(
                    id=str(uuid.uuid4()),
                    section_id=section.id,
                    content_type=content_data.get("content_type", "text"),
                    content=content_data.get("content", ""),
                    position=content_idx + 1
                )
                self.db.add(content)

        # Atualizar o status das preferências do usuário
        try:
            self.update_user_preferences_status(user_id, True)
        except Exception as e:
            # Não queremos que um erro aqui impeça a criação do plano
            logger.error(
                f"Erro ao atualizar status das preferências: {str(e)}")

        # Commitar as mudanças
        self.db.commit()
        self.db.refresh(plan)

        # Adicionar as seções ao plano para retornar
        plan.sections = self.get_sections_by_plan(plan.id)

        return plan

    def get_study_plans_by_user(self, user_id: str) -> List[StudyPlanResponse]:
        """
        Busca todos os planos de estudo de um usuário
        """
        return self.db.query(StudyPlan).filter(StudyPlan.user_id == user_id).all()

    def get_study_plan(self, plan_id: str) -> Optional[StudyPlanResponse]:
        """
        Busca um plano de estudo pelo ID
        """
        return self.db.query(StudyPlan).filter(StudyPlan.id == plan_id).first()

    def get_sections_by_plan(self, plan_id: str) -> List[StudySectionResponse]:
        """
        Busca todas as seções de um plano de estudo
        """
        return self.db.query(StudySection).filter(
            StudySection.study_plan_id == plan_id
        ).order_by(StudySection.position).all()

    def get_section(self, section_id: str) -> Optional[StudySectionResponse]:
        """
        Busca uma seção pelo ID
        """
        return self.db.query(StudySection).filter(StudySection.id == section_id).first()

    def get_section_contents(self, section_id: str) -> List[StudyContentResponse]:
        """
        Busca todos os conteúdos de uma seção
        """
        return self.db.query(StudyContent).filter(
            StudyContent.section_id == section_id
        ).order_by(StudyContent.position).all()

    def update_user_progress(self, user_id: str, progress_data: UserStudyProgressCreate) -> UserStudyProgressResponse:
        """
        Atualiza o progresso do usuário em uma seção
        """
        # Verificar se já existe um registro de progresso para essa seção
        db_progress = self.db.query(UserStudyProgress).filter(
            UserStudyProgress.user_id == user_id,
            UserStudyProgress.section_id == progress_data.section_id
        ).first()

        if db_progress:
            # Atualizar progresso existente
            db_progress.completed = progress_data.completed
            db_progress.user_notes = progress_data.user_notes

            # Se marcado como completo e não tinha data de conclusão anterior, definir agora
            if progress_data.completed and not db_progress.completion_date:
                db_progress.completion_date = datetime.now()

            # Se desmarcado como completo, remover data de conclusão
            if not progress_data.completed:
                db_progress.completion_date = None
        else:
            # Criar novo registro de progresso
            db_progress = UserStudyProgress(
                id=str(uuid.uuid4()),
                user_id=user_id,
                section_id=progress_data.section_id,
                completed=progress_data.completed,
                user_notes=progress_data.user_notes,
                completion_date=datetime.now() if progress_data.completed else None
            )
            self.db.add(db_progress)

        self.db.commit()
        self.db.refresh(db_progress)
        return db_progress

    def save_user_reflection(self, user_id: str, reflection_data: UserReflectionCreate) -> UserReflectionResponse:
        """
        Salva uma reflexão do usuário para uma seção
        """
        db_reflection = UserReflection(
            id=str(uuid.uuid4()),
            user_id=user_id,
            section_id=reflection_data.section_id,
            content=reflection_data.content
        )
        self.db.add(db_reflection)
        self.db.commit()
        self.db.refresh(db_reflection)
        return db_reflection

    def get_user_progress_by_plan(self, user_id: str, plan_id: str) -> Dict[str, UserStudyProgressResponse]:
        """
        Busca o progresso do usuário em todas as seções de um plano de estudo
        """
        # Primeiro, buscar todas as seções do plano
        sections = self.get_sections_by_plan(plan_id)
        section_ids = [section.id for section in sections]

        # Buscar o progresso para cada seção
        progress_entries = self.db.query(UserStudyProgress).filter(
            UserStudyProgress.user_id == user_id,
            UserStudyProgress.section_id.in_(section_ids)
        ).all()

        # Criar um dicionário com o ID da seção como chave e o progresso como valor
        progress_dict = {entry.section_id: entry for entry in progress_entries}
        return progress_dict

    def get_random_devotional(self) -> DailyDevotionalResponse:
        """
        Busca um devocional aleatório para mostrar na página inicial
        """
        # Como ainda não temos uma tabela de devocionais, vamos criar um hardcoded por enquanto
        # Em uma implementação real, buscaríamos da tabela de devocionais

        return {
            "id": str(uuid.uuid4()),
            "title": "Paz em Tempos Difíceis",
            "verse": "Deixo-vos a paz, a minha paz vos dou; não vo-la dou como o mundo a dá. Não se turbe o vosso coração, nem se atemorize.",
            "reference": "João 14:27",
            "reflection": "Jesus nos oferece uma paz que transcende o entendimento humano. Diferente da paz temporária que o mundo oferece, a paz de Cristo é eterna e inabalável, mesmo em meio às tempestades da vida. Hoje, permita que essa paz governe seu coração e afaste toda ansiedade.",
            "created_at": datetime.now()
        }
