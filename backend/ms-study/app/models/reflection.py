from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from app.database.base_class import Base


class Reflection(Base):
    """
    Modelo para as reflexões pessoais feitas pelos usuários durante o estudo.
    Cada reflexão está associada a uma seção específica de um plano de estudo.
    """
    __tablename__ = "reflections"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), nullable=False, index=True)
    section_id = Column(String(36), ForeignKey(
        "study_sections.id", ondelete="CASCADE"), nullable=False)
    reflection_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    section = relationship("StudySection", back_populates="reflections")

    def __repr__(self):
        return f"<Reflection Usuário: {self.user_id}, Seção: {self.section_id}>"
