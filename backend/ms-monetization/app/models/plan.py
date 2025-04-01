from sqlalchemy import Column, String, Integer, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class Plan(Base):
    """Modelo para planos de assinatura"""
    __tablename__ = "plans"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price_monthly = Column(Integer, nullable=False)  # em centavos
    price_yearly = Column(Integer, nullable=False)  # em centavos
    features = Column(JSON, nullable=False)  # recursos do plano
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)
