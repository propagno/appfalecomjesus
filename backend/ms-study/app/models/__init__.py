from app.models.study_plan import StudyPlan
from app.models.study_section import StudySection
from app.models.study_content import StudyContent
from app.models.user_study_progress import UserStudyProgress
from app.models.certificate import Certificate

# Para facilitar a importação de todos os modelos
__all__ = [
    "StudyPlan",
    "StudySection",
    "StudyContent",
    "UserStudyProgress",
    "Certificate"
]
