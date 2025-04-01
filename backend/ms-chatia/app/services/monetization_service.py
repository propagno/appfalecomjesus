import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.monetization import (
    Subscription,
    SubscriptionPlan,
    AdReward,
    PaymentIntent
)
from app.services.stripe_service import StripeService
from app.services.hotmart_service import HotmartService

logger = logging.getLogger(__name__)


class MonetizationService:
    """
    Serviço responsável por gerenciar monetização do sistema.

    Inclui:
    - Planos e assinaturas
    - Pagamentos via Stripe e Hotmart
    - Recompensas por anúncios
    - Limites do plano Free

    Attributes:
        db: Sessão do banco de dados
        stripe: Serviço do Stripe
        hotmart: Serviço do Hotmart
    """

    def __init__(self, db: Session):
        """
        Inicializa o serviço de monetização.

        Args:
            db: Sessão do banco de dados
        """
        self.db = db
        self.stripe = StripeService()
        self.hotmart = HotmartService()

    async def list_plans(self) -> List[SubscriptionPlan]:
        """
        Lista planos de assinatura disponíveis.

        Returns:
            Lista de SubscriptionPlan ativos

        Raises:
            HTTPException: Se erro ao listar
        """
        try:
            plans = self.db.query(SubscriptionPlan).filter(
                SubscriptionPlan.active == True
            ).all()
            return plans
        except Exception as e:
            logger.error(f"Error listing plans: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao listar planos"
            )

    async def get_subscription(self, user_id: UUID) -> Optional[Subscription]:
        """
        Retorna assinatura atual do usuário.

        Args:
            user_id: ID do usuário

        Returns:
            Subscription se existir, None se não

        Raises:
            HTTPException: Se erro ao buscar
        """
        try:
            subscription = self.db.query(Subscription).filter(
                Subscription.user_id == user_id,
                Subscription.status == "active"
            ).first()
            return subscription
        except Exception as e:
            logger.error(f"Error getting subscription: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao buscar assinatura"
            )

    async def create_checkout(
        self,
        user_id: UUID,
        plan_id: UUID
    ) -> PaymentIntent:
        """
        Inicia checkout para assinatura Premium.

        Args:
            user_id: ID do usuário
            plan_id: ID do plano

        Returns:
            PaymentIntent com URL de checkout

        Raises:
            HTTPException: Se erro no processo
        """
        try:
            # Busca plano
            plan = self.db.query(SubscriptionPlan).filter(
                SubscriptionPlan.id == plan_id,
                SubscriptionPlan.active == True
            ).first()

            if not plan:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Plano não encontrado"
                )

            # Cria sessão no Stripe
            payment_intent = await self.stripe.create_checkout_session(
                user_id=user_id,
                plan_id=plan_id,
                amount=int(plan.price * 100)  # Centavos
            )

            # Salva intent
            db_intent = PaymentIntent(
                id=payment_intent.id,
                user_id=user_id,
                plan_id=plan_id,
                amount=payment_intent.amount,
                status=payment_intent.status,
                checkout_url=payment_intent.url,
                created_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(minutes=30)
            )
            self.db.add(db_intent)
            self.db.commit()

            return db_intent

        except HTTPException as he:
            raise he
        except Exception as e:
            logger.error(f"Error creating checkout: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar checkout"
            )

    async def process_webhook(self, payload: Dict) -> None:
        """
        Processa webhook de pagamento.

        Args:
            payload: Dados do webhook

        Raises:
            HTTPException: Se erro no processamento
        """
        try:
            # Identifica origem (Stripe/Hotmart)
            if "type" in payload:  # Stripe
                await self._process_stripe_webhook(payload)
            elif "event" in payload:  # Hotmart
                await self._process_hotmart_webhook(payload)
            else:
                raise ValueError("Webhook inválido")

        except Exception as e:
            logger.error(f"Error processing webhook: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao processar webhook"
            )

    async def register_ad_reward(
        self,
        user_id: UUID,
        ad_type: str
    ) -> AdReward:
        """
        Registra recompensa por visualização de anúncio.

        Args:
            user_id: ID do usuário
            ad_type: Tipo do anúncio

        Returns:
            AdReward criada

        Raises:
            HTTPException: Se erro ao registrar
        """
        try:
            # Verifica limite diário
            today = datetime.utcnow().date()
            rewards_today = self.db.query(AdReward).filter(
                AdReward.user_id == user_id,
                AdReward.watched_at >= today
            ).count()

            if rewards_today >= settings.MAX_DAILY_AD_REWARDS:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Limite diário de recompensas atingido"
                )

            # Cria recompensa
            reward = AdReward(
                user_id=user_id,
                ad_type=ad_type,
                reward_type="chat",  # Ou study/points
                reward_value=5,  # +5 mensagens
                watched_at=datetime.utcnow()
            )
            self.db.add(reward)
            self.db.commit()

            return reward

        except HTTPException as he:
            raise he
        except Exception as e:
            logger.error(f"Error registering ad reward: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao registrar recompensa"
            )

    async def get_remaining_rewards(self, user_id: UUID) -> int:
        """
        Retorna quantidade de recompensas ainda disponíveis hoje.

        Args:
            user_id: ID do usuário

        Returns:
            Número de recompensas restantes

        Raises:
            HTTPException: Se erro ao buscar
        """
        try:
            today = datetime.utcnow().date()
            rewards_today = self.db.query(AdReward).filter(
                AdReward.user_id == user_id,
                AdReward.watched_at >= today
            ).count()

            return settings.MAX_DAILY_AD_REWARDS - rewards_today

        except Exception as e:
            logger.error(f"Error getting remaining rewards: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao buscar recompensas restantes"
            )

    async def _process_stripe_webhook(self, payload: Dict) -> None:
        """
        Processa webhook do Stripe.

        Args:
            payload: Dados do webhook

        Raises:
            Exception: Se erro no processamento
        """
        event_type = payload["type"]

        if event_type == "payment_intent.succeeded":
            # Ativa assinatura
            payment_intent = payload["data"]["object"]
            await self._activate_subscription(
                payment_intent["metadata"]["user_id"],
                payment_intent["metadata"]["plan_id"]
            )
        elif event_type == "payment_intent.payment_failed":
            # Cancela intent
            payment_intent = payload["data"]["object"]
            await self._cancel_payment_intent(payment_intent["id"])

    async def _process_hotmart_webhook(self, payload: Dict) -> None:
        """
        Processa webhook do Hotmart.

        Args:
            payload: Dados do webhook

        Raises:
            Exception: Se erro no processamento
        """
        event = payload["event"]

        if event == "PURCHASE_APPROVED":
            # Ativa assinatura
            await self._activate_subscription(
                payload["data"]["buyer"]["email"],
                payload["data"]["product"]["id"]
            )
        elif event == "PURCHASE_CANCELED":
            # Cancela assinatura
            await self._cancel_subscription(
                payload["data"]["buyer"]["email"]
            )

    async def _activate_subscription(
        self,
        user_id: UUID,
        plan_id: UUID
    ) -> None:
        """
        Ativa assinatura após pagamento confirmado.

        Args:
            user_id: ID do usuário
            plan_id: ID do plano

        Raises:
            Exception: Se erro na ativação
        """
        # Busca plano
        plan = self.db.query(SubscriptionPlan).filter(
            SubscriptionPlan.id == plan_id
        ).first()

        if not plan:
            raise Exception("Plano não encontrado")

        # Cria assinatura
        subscription = Subscription(
            user_id=user_id,
            plan_id=plan_id,
            status="active",
            started_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(
                days=30 if plan.interval == "mensal" else 365
            )
        )
        self.db.add(subscription)
        self.db.commit()

    async def _cancel_payment_intent(self, intent_id: str) -> None:
        """
        Cancela intent de pagamento após falha.

        Args:
            intent_id: ID do payment intent

        Raises:
            Exception: Se erro no cancelamento
        """
        intent = self.db.query(PaymentIntent).filter(
            PaymentIntent.id == intent_id
        ).first()

        if intent:
            intent.status = "canceled"
            self.db.commit()

    async def _cancel_subscription(self, user_id: UUID) -> None:
        """
        Cancela assinatura ativa do usuário.

        Args:
            user_id: ID do usuário

        Raises:
            Exception: Se erro no cancelamento
        """
        subscription = self.db.query(Subscription).filter(
            Subscription.user_id == user_id,
            Subscription.status == "active"
        ).first()

        if subscription:
            subscription.status = "canceled"
            subscription.canceled_at = datetime.utcnow()
            self.db.commit()
