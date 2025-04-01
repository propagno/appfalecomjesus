from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import enum


# Enums para melhor validação
class SubscriptionStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELED = "canceled"
    PENDING = "pending"
    TRIAL = "trial"


class SubscriptionPlanEnum(str, enum.Enum):
    FREE = "free"
    MONTHLY = "monthly"
    ANNUAL = "annual"


class PaymentGatewayEnum(str, enum.Enum):
    STRIPE = "stripe"
    HOTMART = "hotmart"
    NONE = "none"


class RewardTypeEnum(str, enum.Enum):
    CHAT_MESSAGES = "chat_messages"
    STUDY_DAYS = "study_days"
    POINTS = "points"


class TransactionStatusEnum(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    DISPUTED = "disputed"


# Subscription Plan Schemas
class SubscriptionPlanBase(BaseModel):
    name: str
    display_name: str
    description: str
    price: float = 0.0
    currency: str = "BRL"
    duration_days: int = 30
    benefits: Dict[str, Any] = {}
    is_active: bool = True
    trial_days: int = 0
    sort_order: int = 0


class SubscriptionPlanCreate(SubscriptionPlanBase):
    pass


class SubscriptionPlanUpdate(BaseModel):
    display_name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    duration_days: Optional[int] = None
    benefits: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    trial_days: Optional[int] = None
    sort_order: Optional[int] = None


class SubscriptionPlanDB(SubscriptionPlanBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


# Subscription Schemas
class SubscriptionBase(BaseModel):
    user_id: str
    plan_type: SubscriptionPlanEnum = SubscriptionPlanEnum.FREE
    status: SubscriptionStatusEnum = SubscriptionStatusEnum.ACTIVE
    payment_gateway: PaymentGatewayEnum = PaymentGatewayEnum.NONE
    gateway_subscription_id: Optional[str] = None
    amount: float = 0.0
    currency: str = "BRL"
    is_auto_renew: bool = True


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(BaseModel):
    plan_type: Optional[SubscriptionPlanEnum] = None
    status: Optional[SubscriptionStatusEnum] = None
    payment_gateway: Optional[PaymentGatewayEnum] = None
    gateway_subscription_id: Optional[str] = None
    next_payment_date: Optional[datetime] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    is_auto_renew: Optional[bool] = None
    canceled_at: Optional[datetime] = None


class SubscriptionDB(SubscriptionBase):
    id: int
    last_payment_date: Optional[datetime] = None
    next_payment_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    canceled_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True


# Ad Reward Schemas
class AdRewardBase(BaseModel):
    user_id: str
    ad_provider: str
    ad_id: Optional[str] = None
    reward_type: RewardTypeEnum
    reward_value: int = 5
    status: str = "completed"
    ip_address: Optional[str] = None


class AdRewardCreate(AdRewardBase):
    pass


class AdRewardDB(AdRewardBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


# Payment Transaction Schemas
class PaymentTransactionBase(BaseModel):
    user_id: str
    subscription_id: Optional[int] = None
    transaction_id: str
    payment_gateway: PaymentGatewayEnum
    transaction_type: str
    amount: float
    currency: str = "BRL"
    status: TransactionStatusEnum = TransactionStatusEnum.PENDING
    error_message: Optional[str] = None
    transaction_metadata: Optional[Dict[str, Any]] = None


class PaymentTransactionCreate(PaymentTransactionBase):
    pass


class PaymentTransactionUpdate(BaseModel):
    status: Optional[TransactionStatusEnum] = None
    error_message: Optional[str] = None
    transaction_metadata: Optional[Dict[str, Any]] = None


class PaymentTransactionDB(PaymentTransactionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


# API Request and Response Models
class SubscriptionStatusResponse(BaseModel):
    plan_type: str
    status: str
    is_premium: bool
    expiration_date: Optional[datetime] = None
    features: Dict[str, Any] = Field(default_factory=dict)
    chat_messages_per_day: int = 5  # Default para plano Free
    remaining_chat_messages: Optional[int] = None


class AdWatchedRequest(BaseModel):
    ad_provider: str = "google"
    ad_id: Optional[str] = None
    reward_type: RewardTypeEnum = RewardTypeEnum.CHAT_MESSAGES
    ip_address: Optional[str] = None


class AdWatchedResponse(BaseModel):
    success: bool
    reward_type: str
    reward_value: int
    message: str
    updated_chat_limit: Optional[int] = None


class CreateCheckoutSessionRequest(BaseModel):
    plan_type: SubscriptionPlanEnum
    success_url: str
    cancel_url: str


class CreateCheckoutSessionResponse(BaseModel):
    checkout_url: str
    session_id: str
    expires_at: datetime


class WebhookVerificationResponse(BaseModel):
    success: bool
    message: str
    event_type: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
