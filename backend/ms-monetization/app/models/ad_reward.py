from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import enum
import uuid
from datetime import datetime
from enum import Enum as PyEnum

Base = declarative_base()


class AdType(str, PyEnum):
    """Tipos de anúncios suportados pelo sistema."""
    VIDEO = "video"
    BANNER = "banner"
    INTERACTIVE = "interactive"


class RewardType(str, PyEnum):
    """Tipos de recompensas disponíveis no sistema."""
    CHAT_MESSAGES = "chat_messages"
    STUDY_DAYS = "study_days"
    POINTS = "points"


class AdProvider(str, enum.Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"
    INTERNAL = "internal"


class AdReward(Base):
    """
    Modelo para registro de recompensas por visualização de anúncios.

    Armazena informações sobre anúncios visualizados pelos usuários e as
    recompensas concedidas (como mensagens adicionais no chat, dias de estudo, etc).
    """
    __tablename__ = "ad_rewards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, index=True)
    ad_type = Column(Enum(AdType), nullable=False)
    reward_type = Column(Enum(RewardType), nullable=False)
    reward_value = Column(Integer, nullable=False)
    ad_provider = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=True)
    ip_address = Column(String, nullable=True)  # Para análise anti-fraude
    watched_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<AdReward id={self.id}, user_id={self.user_id}, reward_type={self.reward_type}, value={self.reward_value}>"
