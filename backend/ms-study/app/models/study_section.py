from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from app.database.base_class import Base


class StudySection(Base):
    """
    Modelo para as seções dentro de um plano de estudo.
    Cada seção representa uma unidade de estudo dentro do plano.
    """
    __tablename__ = "study_sections"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    study_plan_id = Column(String(36), ForeignKey(
        "study_plans.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    position = Column(Integer, nullable=False)  # ordem dentro do plano
    duration_minutes = Column(Integer, nullable=False, default=20)
    # referência bíblica opcional
    bible_reference = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    study_plan = relationship("StudyPlan", back_populates="sections")
    contents = relationship(
        "StudyContent", back_populates="section", cascade="all, delete-orphan")
    reflections = relationship("Reflection", back_populates="section")

    def __repr__(self):
        return f"<StudySection {self.title} (Plano: {self.study_plan_id})>"
