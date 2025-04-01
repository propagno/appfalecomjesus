from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from app.database.base_class import Base


class UserStudyProgress(Base):
    """
    Modelo para o progresso do usuário em um plano de estudo.
    Rastreia o progresso geral e a seção atual que o usuário está estudando.
    """
    __tablename__ = "user_study_progress"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), nullable=False, index=True)
    study_plan_id = Column(String(36), ForeignKey(
        "study_plans.id", ondelete="CASCADE"), nullable=False)
    current_section_id = Column(String(36), ForeignKey(
        "study_sections.id", ondelete="SET NULL"), nullable=True)
    completion_percentage = Column(Float, nullable=False, default=0.0)
    last_activity_date = Column(
        DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Índice composto para busca rápida de progresso
    __table_args__ = (
        # Índice para buscar progresso por usuário + plano
        {'postgresql_partition_by': 'LIST (user_id)'}
    )

    # Relacionamentos
    study_plan = relationship("StudyPlan", back_populates="user_progress")
    current_section = relationship("StudySection")

    def __repr__(self):
        return f"<UserStudyProgress Usuário: {self.user_id}, Plano: {self.study_plan_id}, Progresso: {self.completion_percentage}%>"
