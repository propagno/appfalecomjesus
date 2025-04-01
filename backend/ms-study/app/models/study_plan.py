from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from app.database.base_class import Base


class StudyPlan(Base):
    """
    Modelo para os planos de estudo disponíveis na plataforma.
    Cada plano pode ser geral ou específico para um usuário.
    """
    __tablename__ = "study_plans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True, index=True)
    # iniciante, intermediário, avançado
    difficulty = Column(String(50), nullable=True)
    duration_days = Column(Integer, nullable=False, default=7)
    image_url = Column(String(500), nullable=True)
    # se true, disponível para todos
    is_public = Column(Boolean, default=False)
    # null se plano padrão
    user_id = Column(String(36), index=True, nullable=True)
    created_by_ia = Column(Boolean, default=False)  # se foi gerado por IA
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    sections = relationship(
        "StudySection", back_populates="study_plan", cascade="all, delete-orphan")
    user_progress = relationship(
        "UserStudyProgress", back_populates="study_plan")

    def __repr__(self):
        return f"<StudyPlan {self.title}>"
