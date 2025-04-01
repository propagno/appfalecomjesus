import uuid
from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.db.session import Base


class PointHistory(Base):
    """Modelo para armazenar o histórico de transações de pontos"""

    __tablename__ = "point_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, index=True)

    # Categoria de pontos (estudo_diario, chat_ia, reflexao, etc)
    category = Column(String, nullable=False, index=True)

    # Quantidade de pontos desta transação (pode ser positivo ou negativo)
    amount = Column(Integer, nullable=False)

    # Fonte da ação (completar_estudo, responder_chat, assistir_ad, etc)
    action = Column(String, nullable=False)

    # Descrição detalhada da ação (opcional)
    description = Column(Text, nullable=True)

    # ID da entidade relacionada (estudo_id, chat_id, etc)
    related_entity_id = Column(String, nullable=True)

    # Data e hora da transação
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PointHistory(user_id={self.user_id}, category={self.category}, amount={self.amount}, action={self.action})>"
