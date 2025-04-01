from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from app.models.subscription import SubscriptionStatus, SubscriptionPlan, PaymentGateway


class SubscriptionBase(BaseModel):
    """Schema base para assinaturas."""
    plan_type: SubscriptionPlan = Field(..., description="Tipo de plano")


class SubscriptionCreate(SubscriptionBase):
    """Schema para criação de assinatura."""
    status: SubscriptionStatus = Field(
        default=SubscriptionStatus.PENDING, description="Status da assinatura")
    payment_gateway: PaymentGateway = Field(...,
                                            description="Gateway de pagamento")
    amount: Optional[float] = Field(None, description="Valor da assinatura")
    currency: Optional[str] = Field(None, description="Moeda da assinatura")
    is_auto_renew: Optional[bool] = Field(
        True, description="Se a assinatura renova automaticamente")


class SubscriptionUpdate(BaseModel):
    """Schema para atualização de assinatura."""
    status: Optional[SubscriptionStatus] = Field(
        None, description="Status da assinatura")
    next_payment_date: Optional[datetime] = Field(
        None, description="Data do próximo pagamento")
    last_payment_date: Optional[datetime] = Field(
        None, description="Data do último pagamento")
    amount: Optional[float] = Field(None, description="Valor da assinatura")
    currency: Optional[str] = Field(None, description="Moeda da assinatura")
    is_auto_renew: Optional[bool] = Field(
        None, description="Se a assinatura renova automaticamente")
    expires_at: Optional[datetime] = Field(
        None, description="Data de expiração da assinatura")


class SubscriptionResponse(SubscriptionBase):
    """Schema para resposta de assinatura."""
    id: UUID
    user_id: str
    status: SubscriptionStatus
    payment_gateway: PaymentGateway
    last_payment_date: Optional[datetime] = None
    next_payment_date: Optional[datetime] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    is_auto_renew: bool
    expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class SubscriptionList(BaseModel):
    """Schema para listagem de assinaturas."""
    items: List[SubscriptionResponse]
    count: int

    class Config:
        orm_mode = True
