from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.study import StudyPlan, StudySection, StudyContent, UserStudyProgress
from app.schemas.study import (
    StudyPlanCreate,
    StudySectionCreate,
    StudyContentCreate,
    UserStudyProgressCreate
)


class StudyService:
    """Serviço para gerenciar estudos e planos"""

    @staticmethod
    async def create_study_plan(
        db: Session,
        user_id: str,
        plan: StudyPlanCreate
    ) -> StudyPlan:
        """
        Cria um novo plano de estudo.
        """
        db_plan = StudyPlan(
            user_id=user_id,
            **plan.model_dump()
        )
        db.add(db_plan)
        db.commit()
        db.refresh(db_plan)
        return db_plan

    @staticmethod
    async def get_study_plan(
        db: Session,
        plan_id: str
    ) -> Optional[StudyPlan]:
        """
        Obtém um plano de estudo específico.
        """
        return db.query(StudyPlan).filter(StudyPlan.id == plan_id).first()

    @staticmethod
    async def get_user_study_plans(
        db: Session,
        user_id: str
    ) -> List[StudyPlan]:
        """
        Lista todos os planos de estudo do usuário.
        """
        return db.query(StudyPlan).filter(StudyPlan.user_id == user_id).all()

    @staticmethod
    async def create_study_section(
        db: Session,
        study_plan_id: str,
        section: StudySectionCreate
    ) -> StudySection:
        """
        Cria uma nova seção de estudo.
        """
        db_section = StudySection(
            study_plan_id=study_plan_id,
            **section.model_dump()
        )
        db.add(db_section)
        db.commit()
        db.refresh(db_section)
        return db_section

    @staticmethod
    async def create_study_content(
        db: Session,
        section_id: str,
        content: StudyContentCreate
    ) -> StudyContent:
        """
        Cria um novo conteúdo de estudo.
        """
        db_content = StudyContent(
            section_id=section_id,
            **content.model_dump()
        )
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        return db_content

    @staticmethod
    async def get_current_study(
        db: Session,
        user_id: str
    ) -> Optional[Dict]:
        """
        Obtém o estudo atual do usuário.
        """
        progress = db.query(UserStudyProgress).filter(
            UserStudyProgress.user_id == user_id
        ).first()

        if not progress:
            return None

        plan = await StudyService.get_study_plan(db, progress.study_plan_id)
        if not plan:
            return None

        current_section = None
        if progress.current_section_id:
            current_section = db.query(StudySection).filter(
                StudySection.id == progress.current_section_id
            ).first()

        return {
            "plan": plan,
            "current_section": current_section,
            "progress": progress
        }

    @staticmethod
    async def update_study_progress(
        db: Session,
        user_id: str,
        progress: UserStudyProgressCreate
    ) -> UserStudyProgress:
        """
        Atualiza o progresso do usuário no estudo.
        """
        db_progress = db.query(UserStudyProgress).filter(
            UserStudyProgress.user_id == user_id,
            UserStudyProgress.study_plan_id == progress.study_plan_id
        ).first()

        if not db_progress:
            db_progress = UserStudyProgress(
                user_id=user_id,
                **progress.model_dump()
            )
            db.add(db_progress)
        else:
            for field, value in progress.model_dump().items():
                setattr(db_progress, field, value)
            db_progress.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(db_progress)
        return db_progress

    @staticmethod
    async def get_study_progress(
        db: Session,
        user_id: str,
        study_plan_id: str
    ) -> Optional[UserStudyProgress]:
        """
        Obtém o progresso do usuário em um plano específico.
        """
        return db.query(UserStudyProgress).filter(
            UserStudyProgress.user_id == user_id,
            UserStudyProgress.study_plan_id == study_plan_id
        ).first()
