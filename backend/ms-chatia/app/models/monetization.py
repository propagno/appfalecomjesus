from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class SubscriptionPlan(Base):
    """
    Modelo para planos de assinatura disponíveis.

    Representa os diferentes planos que podem ser assinados:
    - Free (gratuito)
    - Premium Mensal
    - Premium Anual

    Attributes:
        id: Identificador único do plano
        name: Nome do plano
        description: Descrição detalhada
        price: Preço em reais
        interval: Intervalo (mensal/anual)
        features: Lista de funcionalidades
        active: Se está disponível
        created_at: Data de criação
        discount_percent: Desconto atual
        subscriptions: Relacionamento com assinaturas
    """
    __tablename__ = "subscription_plans"

    id = Column(PgUUID, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    interval = Column(String, nullable=False)  # mensal, anual
    features = Column(String, nullable=False)  # JSON array
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    discount_percent = Column(Integer, nullable=True)

    # Relacionamentos
    subscriptions = relationship("Subscription", back_populates="plan")


class Subscription(Base):
    """
    Modelo para assinaturas de usuários.

    Registra assinaturas ativas e histórico:
    - Plano atual
    - Status (ativo/cancelado)
    - Datas importantes
    - Método de pagamento

    Attributes:
        id: Identificador único da assinatura
        user_id: ID do usuário assinante
        plan_id: ID do plano assinado
        status: Status atual
        payment_method: Método de pagamento
        started_at: Data de início
        expires_at: Data de expiração
        canceled_at: Data de cancelamento
        auto_renew: Se renova automaticamente
        plan: Relacionamento com plano
        payment_history: Histórico de pagamentos
    """
    __tablename__ = "subscriptions"

    id = Column(PgUUID, primary_key=True)
    user_id = Column(PgUUID, nullable=False)
    plan_id = Column(PgUUID, ForeignKey(
        "subscription_plans.id"), nullable=False)
    status = Column(String, nullable=False)  # active, canceled
    payment_method = Column(String, nullable=False)  # stripe, hotmart
    started_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    canceled_at = Column(DateTime, nullable=True)
    auto_renew = Column(Boolean, default=True)

    # Relacionamentos
    plan = relationship("SubscriptionPlan", back_populates="subscriptions")
    payment_history = relationship(
        "PaymentHistory", back_populates="subscription")


class PaymentHistory(Base):
    """
    Modelo para histórico de pagamentos.

    Registra todas as transações:
    - Pagamentos aprovados
    - Tentativas falhas
    - Reembolsos
    - Renovações

    Attributes:
        id: Identificador único do pagamento
        subscription_id: ID da assinatura
        amount: Valor em centavos
        currency: Moeda (BRL)
        status: Status do pagamento
        payment_method: Método usado
        transaction_id: ID externo
        created_at: Data da transação
        subscription: Relacionamento com assinatura
    """
    __tablename__ = "payment_history"

    id = Column(PgUUID, primary_key=True)
    subscription_id = Column(PgUUID, ForeignKey(
        "subscriptions.id"), nullable=False)
    amount = Column(Integer, nullable=False)  # Centavos
    currency = Column(String, default="BRL")
    status = Column(String, nullable=False)  # success, failed, refunded
    payment_method = Column(String, nullable=False)
    transaction_id = Column(String, nullable=False)  # ID no Stripe/Hotmart
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    subscription = relationship(
        "Subscription", back_populates="payment_history")


class PaymentIntent(Base):
    """
    Modelo para intenções de pagamento.

    Registra tentativas de checkout:
    - URL de pagamento
    - Status da tentativa
    - Validade do link

    Attributes:
        id: Identificador único da intenção
        user_id: ID do usuário
        plan_id: ID do plano
        amount: Valor em centavos
        currency: Moeda (BRL)
        status: Status da intenção
        checkout_url: URL de pagamento
        created_at: Data de criação
        expires_at: Data de expiração
    """
    __tablename__ = "payment_intents"

    id = Column(PgUUID, primary_key=True)
    user_id = Column(PgUUID, nullable=False)
    plan_id = Column(PgUUID, ForeignKey(
        "subscription_plans.id"), nullable=False)
    amount = Column(Integer, nullable=False)  # Centavos
    currency = Column(String, default="BRL")
    status = Column(String, nullable=False)  # pending, completed, canceled
    checkout_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)


class AdReward(Base):
    """
    Modelo para recompensas por anúncios.

    Registra visualizações de anúncios:
    - Tipo do anúncio
    - Recompensa concedida
    - Status da aplicação

    Attributes:
        id: Identificador único da recompensa
        user_id: ID do usuário
        ad_type: Tipo do anúncio
        reward_type: Tipo da recompensa
        reward_value: Valor da recompensa
        watched_at: Data da visualização
        applied: Se foi aplicada
        applied_at: Data da aplicação
    """
    __tablename__ = "ad_rewards"

    id = Column(PgUUID, primary_key=True)
    user_id = Column(PgUUID, nullable=False)
    ad_type = Column(String, nullable=False)  # video, banner
    reward_type = Column(String, nullable=False)  # chat, study, points
    reward_value = Column(Integer, nullable=False)  # +5, +1, +10
    watched_at = Column(DateTime, default=datetime.utcnow)
    applied = Column(Boolean, default=False)
    applied_at = Column(DateTime, nullable=True)
