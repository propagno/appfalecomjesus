from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()


class SubscriptionStatus(str, enum.Enum):
    """Status possíveis de uma assinatura"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELED = "canceled"
    PENDING = "pending"
    TRIAL = "trial"
    PAST_DUE = "past_due"  # Status para pagamento atrasado


class SubscriptionPlan(str, enum.Enum):
    FREE = "free"
    MONTHLY = "monthly"
    ANNUAL = "annual"


class PaymentGateway(str, enum.Enum):
    """Gateways de pagamento suportados"""
    STRIPE = "stripe"
    HOTMART = "hotmart"
    NONE = "none"


class Subscription(Base):
    """Modelo para assinaturas de usuários"""
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, unique=True)
    plan_type = Column(String, default=SubscriptionPlan.FREE)
    status = Column(String, default=SubscriptionStatus.ACTIVE)
    payment_gateway = Column(String, default=PaymentGateway.NONE)
    gateway_subscription_id = Column(String, nullable=True)
    last_payment_date = Column(DateTime(timezone=True), nullable=True)
    next_payment_date = Column(DateTime(timezone=True), nullable=True)
    # Data de expiração da assinatura
    expires_at = Column(DateTime(timezone=True), nullable=True)
    amount = Column(Float, default=0.0)
    currency = Column(String, default="BRL")
    is_auto_renew = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        onupdate=func.now(), server_default=func.now())
    canceled_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Subscription(id={self.id}, user_id={self.user_id}, plan={self.plan_type}, status={self.status})>"
