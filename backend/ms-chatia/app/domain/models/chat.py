import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.infrastructure.database import Base


class ChatHistory(Base):
    """
    Modelo para armazenar o histórico de mensagens do chat com a IA.
    """
    __tablename__ = "chat_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    model_used = Column(String(50), nullable=False)
    context = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(
        self,
        user_id: uuid.UUID,
        message: str,
        response: str,
        model_used: str,
        context: str = None
    ):
        self.id = uuid.uuid4()
        self.user_id = user_id
        self.message = message
        self.response = response
        self.model_used = model_used
        self.context = context


class ChatMessage(Base):
    """
    Modelo para armazenar mensagens e respostas do chat
    """
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, index=True, nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    model_used = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ChatMessage: {self.id}>"
