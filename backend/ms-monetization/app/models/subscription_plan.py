from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # free, monthly, annual
    display_name = Column(String)  # Nome exibido para o usuário
    description = Column(Text)
    price = Column(Float, default=0.0)
    currency = Column(String, default="BRL")
    duration_days = Column(Integer, default=30)  # 30, 365
    # Lista de benefícios do plano: {"unlimited_chat": true, "ad_free": true}
    benefits = Column(JSON)
    is_active = Column(Boolean, default=True)
    trial_days = Column(Integer, default=0)  # Dias de teste gratuito
    sort_order = Column(Integer, default=0)  # Para ordenação na UI
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<SubscriptionPlan(id={self.id}, name={self.name}, price={self.price})>"
