from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base
import uuid
import enum


class PlanType(str, enum.Enum):
    FREE = "free"
    MONTHLY = "mensal"
    ANNUAL = "anual"


class PaymentGateway(str, enum.Enum):
    STRIPE = "Stripe"
    HOTMART = "Hotmart"


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        "users.id"), nullable=False)
    plan_type = Column(Enum(PlanType), nullable=False, default=PlanType.FREE)
    started_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    payment_gateway = Column(Enum(PaymentGateway), nullable=True)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True),
                        onupdate=func.now(), nullable=True)


class AdReward(Base):
    __tablename__ = "ad_rewards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        "users.id"), nullable=False)
    message_bonus = Column(Integer, nullable=False)
    ad_provider = Column(String, nullable=False)
    watched_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
