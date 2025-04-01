from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from app.database.base_class import Base


class Certificate(Base):
    """
    Modelo para os certificados de conclusão dos planos de estudo.
    Um certificado é gerado quando o usuário completa 100% de um plano.
    """
    __tablename__ = "certificates"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), nullable=False, index=True)
    study_plan_id = Column(String(36), ForeignKey(
        "study_plans.id", ondelete="CASCADE"), nullable=False)
    certificate_code = Column(
        String(50), nullable=False, unique=True, index=True)
    completion_date = Column(DateTime(timezone=True), nullable=False)
    download_count = Column(Integer, nullable=False, default=0)
    # Versículo de inspiração
    verse_reference = Column(String(100), nullable=True)
    verse_text = Column(Text, nullable=True)  # Texto do versículo
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    study_plan = relationship("StudyPlan")

    def __repr__(self):
        return f"<Certificate Usuário: {self.user_id}, Plano: {self.study_plan_id}, Código: {self.certificate_code}>"
