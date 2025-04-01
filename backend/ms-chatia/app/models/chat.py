import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


class ChatHistory(Base):
    """
    Modelo para armazenamento do histórico de conversas do chat com a IA
    """
    __tablename__ = "chat_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    model_used = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ChatHistory(id={self.id}, user_id={self.user_id})>"

    def to_dict(self):
        """
        Converte o objeto para um dicionário
        """
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "message": self.message,
            "response": self.response,
            "model_used": self.model_used,
            "created_at": self.created_at.isoformat()
        }
