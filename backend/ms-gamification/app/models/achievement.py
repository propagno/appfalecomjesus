import uuid
from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime

from app.db.session import Base


class Achievement(Base):
    """Modelo para armazenar as definições de conquistas disponíveis no sistema"""

    __tablename__ = "achievements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Identificador único da conquista (slug)
    code = Column(String, nullable=False, unique=True, index=True)

    # Nome da conquista
    name = Column(String, nullable=False)

    # Descrição da conquista
    description = Column(Text, nullable=False)

    # Categoria da conquista (estudo, social, reflexao, etc)
    category = Column(String, nullable=False, index=True)

    # Dificuldade da conquista (facil, medio, dificil)
    difficulty = Column(String, nullable=False, index=True)

    # Pontos necessários para desbloquear a conquista
    points_required = Column(Integer, nullable=False, default=0)

    # Critérios adicionais em formato JSON (opcional)
    criteria = Column(JSONB, nullable=True)

    # URL da imagem da conquista (selo/badge)
    image_url = Column(String, nullable=True)

    # Pontos de recompensa ao desbloquear
    reward_points = Column(Integer, nullable=False, default=0)

    # Conquista oculta (revelada apenas quando desbloqueada)
    is_hidden = Column(Boolean, nullable=False, default=False)

    # Controle de timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Achievement(code={self.code}, name={self.name}, category={self.category})>"
