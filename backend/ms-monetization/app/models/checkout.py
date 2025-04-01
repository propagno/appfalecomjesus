from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class CheckoutSession(Base):
    """Modelo para sessões de checkout"""
    __tablename__ = "checkout_sessions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    session_id = Column(String, unique=True, nullable=False)
    payment_gateway = Column(String, nullable=False)  # stripe ou hotmart
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, default="pending")  # pending, completed, failed
    payment_id = Column(String, nullable=True)  # ID do pagamento no gateway
    # Mensagem de erro em caso de falha
    error_message = Column(String, nullable=True)
