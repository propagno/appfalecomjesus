import uuid
from sqlalchemy import Column, String, DateTime, Boolean, JSON, ForeignKey, Enum
from sqlalchemy.sql import func
from app.infrastructure.database import Base
import enum


class SubscriptionType(enum.Enum):
    FREE = "free"
    PREMIUM = "premium"


class SubscriptionStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"
    PENDING = "pending"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True,
                default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    onboarding_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User {self.email}>"


class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(String, primary_key=True, index=True,
                default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    objectives = Column(JSON, nullable=False)
    bible_experience_level = Column(String, nullable=False)
    content_preferences = Column(JSON, nullable=False)
    preferred_time = Column(String, nullable=False)
    onboarding_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<UserPreferences for user {self.user_id}>"


class UserSubscription(Base):
    __tablename__ = "user_subscriptions"

    id = Column(String, primary_key=True, index=True,
                default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    subscription_type = Column(
        Enum(SubscriptionType), nullable=False, default=SubscriptionType.FREE)
    status = Column(Enum(SubscriptionStatus), nullable=False,
                    default=SubscriptionStatus.ACTIVE)
    payment_gateway = Column(String, nullable=True)
    expiration_date = Column(DateTime(timezone=True), nullable=True)
    last_payment_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<UserSubscription for user {self.user_id}: {self.subscription_type.value} - {self.status.value}>"
