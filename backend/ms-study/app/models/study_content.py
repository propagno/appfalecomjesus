from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from app.database.base_class import Base


class StudyContent(Base):
    """
    Modelo para os conteúdos dentro de uma seção de estudo.
    Cada conteúdo pode ser texto, áudio, vídeo ou outro formato.
    """
    __tablename__ = "study_contents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    section_id = Column(String(36), ForeignKey(
        "study_sections.id", ondelete="CASCADE"), nullable=False)
    # text, audio, video, question, etc.
    content_type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)  # texto ou URL para recurso
    position = Column(Integer, nullable=False)  # ordem dentro da seção
    # título opcional para o conteúdo
    title = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    section = relationship("StudySection", back_populates="contents")

    def __repr__(self):
        return f"<StudyContent {self.content_type} (Seção: {self.section_id}, Pos: {self.position})>"
