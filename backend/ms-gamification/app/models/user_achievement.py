import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.db.session import Base


class UserAchievement(Base):
    """Modelo para armazenar as conquistas obtidas ou em progresso de cada usuário"""

    __tablename__ = "user_achievements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, index=True)

    # Referência à conquista
    achievement_id = Column(UUID(as_uuid=True), ForeignKey(
        "achievements.id", ondelete="CASCADE"), nullable=False)

    # Progresso atual do usuário para esta conquista (porcentagem, 100 = completo)
    progress = Column(Float, nullable=False, default=0)

    # Pontos acumulados para esta conquista
    current_points = Column(Integer, nullable=False, default=0)

    # Data em que a conquista foi desbloqueada (null se não foi desbloqueada ainda)
    unlocked_at = Column(DateTime, nullable=True)

    # Controle de timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    # Chave única composta para evitar duplicação de conquista por usuário
    __table_args__ = (
        {"sqlite_autoincrement": True},
    )

    @property
    def is_unlocked(self):
        """Verifica se a conquista está desbloqueada"""
        return self.unlocked_at is not None

    def __repr__(self):
        return f"<UserAchievement(user_id={self.user_id}, achievement_id={self.achievement_id}, progress={self.progress})>"
