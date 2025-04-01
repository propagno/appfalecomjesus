import uuid
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.db.session import Base


class UserPoint(Base):
    """Modelo para armazenar os pontos acumulados por usuário e categoria"""

    __tablename__ = "user_points"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, index=True)

    # Categoria de pontos (estudo_diario, chat_ia, reflexao, etc)
    category = Column(String, nullable=False, index=True)

    # Quantidade total de pontos nesta categoria
    amount = Column(Integer, nullable=False, default=0)

    # Controle de timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    # Chave única composta para evitar duplicação de categoria por usuário
    __table_args__ = (
        {"sqlite_autoincrement": True},
    )

    def __repr__(self):
        return f"<UserPoint(user_id={self.user_id}, category={self.category}, amount={self.amount})>"
