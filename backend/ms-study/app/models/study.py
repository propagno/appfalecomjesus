from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from app.core.database import Base


class StudyPlan(Base):
    """Modelo para planos de estudo"""
    __tablename__ = "study_plans"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)  # Sem FK para tabela externa
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    duration_days = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)


class StudySection(Base):
    """Modelo para seções de estudo"""
    __tablename__ = "study_sections"

    id = Column(String, primary_key=True)
    study_plan_id = Column(String, ForeignKey(
        "study_plans.id"), nullable=False)
    title = Column(String, nullable=False)
    position = Column(Integer, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class StudyContent(Base):
    """Modelo para conteúdo de estudo"""
    __tablename__ = "study_content"

    id = Column(String, primary_key=True)
    section_id = Column(String, ForeignKey(
        "study_sections.id"), nullable=False)
    content_type = Column(String, nullable=False)  # text, audio, video
    content = Column(Text, nullable=False)
    position = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserStudyProgress(Base):
    """Modelo para progresso do usuário no estudo"""
    __tablename__ = "user_study_progress"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)  # Sem FK para tabela externa
    study_plan_id = Column(String, ForeignKey(
        "study_plans.id"), nullable=False)
    current_section_id = Column(String, ForeignKey(
        "study_sections.id"), nullable=True)
    completion_percentage = Column(Float, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
