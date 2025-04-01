from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class SubscriptionPlanBase(BaseModel):
    """
    Schema base para plano de assinatura.

    Attributes:
        name: Nome do plano (Free, Premium Mensal, Premium Anual)
        description: Descrição detalhada dos benefícios
        price: Preço em reais (0 para Free)
        interval: Intervalo de cobrança (mensal, anual)
        features: Lista de funcionalidades incluídas
    """
    name: str
    description: str
    price: float
    interval: str
    features: List[str]


class SubscriptionPlan(SubscriptionPlanBase):
    """
    Schema completo de plano com ID.

    Attributes:
        id: Identificador único do plano
        created_at: Data de criação do plano
        active: Se o plano está ativo para venda
        discount_percent: Desconto atual em % (se houver)
    """
    id: UUID
    created_at: datetime
    active: bool
    discount_percent: Optional[int] = None

    class Config:
        orm_mode = True


class SubscriptionBase(BaseModel):
    """
    Schema base para assinatura.

    Attributes:
        plan_id: ID do plano assinado
        status: Status atual (ativo, inativo, cancelado)
        payment_method: Método de pagamento usado
    """
    plan_id: UUID
    status: str
    payment_method: str


class Subscription(SubscriptionBase):
    """
    Schema completo de assinatura.

    Attributes:
        id: Identificador único da assinatura
        user_id: ID do usuário assinante
        started_at: Data de início
        expires_at: Data de expiração
        canceled_at: Data de cancelamento (se houver)
        auto_renew: Se renova automaticamente
        payment_history: Histórico de pagamentos
    """
    id: UUID
    user_id: UUID
    started_at: datetime
    expires_at: datetime
    canceled_at: Optional[datetime] = None
    auto_renew: bool = True
    payment_history: List[dict]

    class Config:
        orm_mode = True


class PaymentIntentBase(BaseModel):
    """
    Schema base para intenção de pagamento.

    Attributes:
        plan_id: ID do plano a ser assinado
        payment_method: Método escolhido (cartão, pix, boleto)
        currency: Moeda do pagamento (BRL)
    """
    plan_id: UUID
    payment_method: str
    currency: str = "BRL"


class PaymentIntent(PaymentIntentBase):
    """
    Schema completo de intenção de pagamento.

    Attributes:
        id: Identificador único da intenção
        user_id: ID do usuário pagador
        amount: Valor total em centavos
        status: Status do pagamento
        checkout_url: URL segura para checkout
        created_at: Data de criação
        expires_at: Data de expiração do link
    """
    id: UUID
    user_id: UUID
    amount: int
    status: str
    checkout_url: str
    created_at: datetime
    expires_at: datetime

    class Config:
        orm_mode = True


class AdRewardBase(BaseModel):
    """
    Schema base para recompensa por anúncio.

    Attributes:
        ad_type: Tipo do anúncio assistido
        reward_type: Tipo da recompensa (chat, study, points)
        reward_value: Valor da recompensa (+5 mensagens, +1 dia, +10 pontos)
    """
    ad_type: str
    reward_type: str
    reward_value: int


class AdReward(AdRewardBase):
    """
    Schema completo de recompensa por anúncio.

    Attributes:
        id: Identificador único da recompensa
        user_id: ID do usuário recompensado
        watched_at: Data/hora que assistiu
        applied: Se a recompensa foi aplicada
        applied_at: Quando foi aplicada
    """
    id: UUID
    user_id: UUID
    watched_at: datetime
    applied: bool = False
    applied_at: Optional[datetime] = None

    class Config:
        orm_mode = True
