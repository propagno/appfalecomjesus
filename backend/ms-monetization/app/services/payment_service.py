from typing import Optional, Dict, Any, Tuple
import logging
import json
import httpx
import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import stripe

from app.repositories import PaymentTransactionRepository
from app.services.subscription_service import SubscriptionService
from app.models import (
    TransactionType,
    TransactionStatus,
    SubscriptionStatus,
    PaymentGateway
)
from app.schemas import (
    CreateCheckoutSessionRequest,
    CreateCheckoutSessionResponse,
    WebhookVerificationResponse
)
from app.core.config import settings

# Configurar logger
logger = logging.getLogger(__name__)


class PaymentService:
    def __init__(self, db: Session):
        self.db = db
        self.transaction_repo = PaymentTransactionRepository(db)
        self.subscription_service = SubscriptionService(db)

        # Configurar Stripe
        if settings.STRIPE_API_KEY:
            stripe.api_key = settings.STRIPE_API_KEY

    def create_checkout_session(
        self,
        user_id: str,
        plan_id: str,
        success_url: str,
        cancel_url: str,
        payment_gateway: str
    ) -> str:
        """
        Cria uma sessão de checkout para assinatura.

        Args:
            user_id: ID do usuário
            plan_id: ID do plano (monthly, yearly)
            success_url: URL de redirecionamento em caso de sucesso
            cancel_url: URL de redirecionamento em caso de cancelamento
            payment_gateway: Gateway de pagamento (stripe, hotmart)

        Returns:
            URL de checkout para redirecionamento
        """
        logger.info(
            f"Criando sessão de checkout para usuário {user_id} no plano {plan_id}")

        # Obter os detalhes do plano
        price_id = self._get_price_id_by_plan(plan_id, payment_gateway)

        if payment_gateway.lower() == "stripe":
            return self._create_stripe_checkout(user_id, price_id, success_url, cancel_url)
        elif payment_gateway.lower() == "hotmart":
            return self._create_hotmart_checkout(user_id, plan_id, success_url, cancel_url)
        else:
            logger.error(
                f"Gateway de pagamento não suportado: {payment_gateway}")
            raise ValueError(
                f"Gateway de pagamento não suportado: {payment_gateway}")

    def _create_stripe_checkout(self, user_id: str, price_id: str, success_url: str, cancel_url: str) -> str:
        """
        Cria uma sessão de checkout no Stripe.

        Args:
            user_id: ID do usuário
            price_id: ID do preço no Stripe
            success_url: URL de redirecionamento em caso de sucesso
            cancel_url: URL de redirecionamento em caso de cancelamento

        Returns:
            URL de checkout do Stripe
        """
        logger.info(
            f"Criando sessão de checkout no Stripe para usuário {user_id}")

        try:
            # Criar sessão de checkout no Stripe
            checkout_session = stripe.checkout.Session.create(
                customer_email=user_id,  # Idealmente seria o email do usuário
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1,
                    },
                ],
                mode="subscription",
                success_url=success_url,
                cancel_url=cancel_url,
                client_reference_id=user_id,
                metadata={
                    "user_id": user_id,
                }
            )

            logger.info(f"Sessão de checkout criada: {checkout_session.id}")
            return checkout_session.url
        except Exception as e:
            logger.error(
                f"Erro ao criar sessão de checkout no Stripe: {str(e)}")
            raise ValueError(f"Erro ao criar sessão de checkout: {str(e)}")

    def _create_hotmart_checkout(self, user_id: str, plan_id: str, success_url: str, cancel_url: str) -> str:
        """
        Cria uma URL de checkout no Hotmart.

        Args:
            user_id: ID do usuário
            plan_id: ID do plano (monthly, yearly)
            success_url: URL de redirecionamento em caso de sucesso
            cancel_url: URL de redirecionamento em caso de cancelamento

        Returns:
            URL de checkout do Hotmart
        """
        logger.info(
            f"Criando URL de checkout no Hotmart para usuário {user_id}")

        # Mapear plan_id para product_id do Hotmart
        product_id = self._get_hotmart_product_id(plan_id)

        # Criar URL de checkout do Hotmart
        base_url = settings.HOTMART_CHECKOUT_URL
        checkout_url = f"{base_url}/{product_id}?ref={settings.HOTMART_REFERENCE}&offDiscount=true"

        # Adicionar usuário como parâmetro para identificação no webhook
        checkout_url += f"&src={user_id}"

        logger.info(f"URL de checkout Hotmart criada: {checkout_url}")
        return checkout_url

    def _get_price_id_by_plan(self, plan_id: str, payment_gateway: str) -> str:
        """
        Retorna o ID do preço no gateway de pagamento com base no ID do plano.

        Args:
            plan_id: ID do plano (monthly, yearly)
            payment_gateway: Gateway de pagamento (stripe, hotmart)

        Returns:
            ID do preço no gateway de pagamento
        """
        # Mapear plan_id para price_id do gateway
        if payment_gateway.lower() == "stripe":
            plan_mapping = {
                "monthly": settings.STRIPE_MONTHLY_PRICE_ID,
                "yearly": settings.STRIPE_YEARLY_PRICE_ID,
            }
        elif payment_gateway.lower() == "hotmart":
            # No caso do Hotmart, retornamos o product_id diretamente
            return self._get_hotmart_product_id(plan_id)
        else:
            raise ValueError(
                f"Gateway de pagamento não suportado: {payment_gateway}")

        if plan_id not in plan_mapping:
            logger.error(f"Plano não encontrado: {plan_id}")
            raise ValueError(f"Plano não encontrado: {plan_id}")

        return plan_mapping[plan_id]

    def _get_hotmart_product_id(self, plan_id: str) -> str:
        """
        Retorna o ID do produto no Hotmart com base no ID do plano.

        Args:
            plan_id: ID do plano (monthly, yearly)

        Returns:
            ID do produto no Hotmart
        """
        plan_mapping = {
            "monthly": settings.HOTMART_MONTHLY_PRODUCT_ID,
            "yearly": settings.HOTMART_YEARLY_PRODUCT_ID,
        }

        if plan_id not in plan_mapping:
            logger.error(f"Plano não encontrado: {plan_id}")
            raise ValueError(f"Plano não encontrado: {plan_id}")

        return plan_mapping[plan_id]

    def validate_subscription(self, user_id: str) -> bool:
        """
        Valida se o usuário tem uma assinatura ativa.

        Args:
            user_id: ID do usuário

        Returns:
            True se o usuário tiver uma assinatura ativa, False caso contrário
        """
        logger.info(f"Validando assinatura para usuário {user_id}")

        # Obter assinatura atual do usuário
        subscription = self.subscription_service.get_current_subscription(
            user_id)

        # Verificar se existe e está ativa
        return (
            subscription is not None and
            subscription.status == SubscriptionStatus.ACTIVE
        )

    async def process_stripe_webhook(self, event_type: str, event_data: Dict[str, Any]) -> WebhookVerificationResponse:
        """
        Processa webhooks recebidos do Stripe.
        """
        try:
            # Validar a assinatura do webhook
            # (em produção, teríamos que verificar a assinatura do Stripe)

            # Extrair dados relevantes
            session_id = event_data.get("id", "")
            metadata = event_data.get("metadata", {})
            user_id = metadata.get("user_id", "")
            plan_type = metadata.get("plan_type", "")

            # Buscar a transação relacionada
            transaction = await self.transaction_repo.get_by_transaction_id(session_id)

            if not transaction:
                logger.warning(
                    f"Transação não encontrada para webhook: {session_id}")
                return WebhookVerificationResponse(
                    success=False,
                    message="Transação não encontrada",
                    event_type=event_type
                )

            # Verificar no metadado o tipo de plano para determinar a ação
            if transaction.transaction_metadata and transaction.transaction_metadata.get("plan_type"):
                plan_type = transaction.transaction_metadata.get("plan_type")

            # Processar com base no tipo de evento
            if event_type == "checkout.session.completed":
                # Atualizar status da transação para COMPLETED
                await self.transaction_repo.update_status(
                    transaction.id,
                    TransactionStatus.COMPLETED,
                    metadata=event_data
                )

                # Extrair usuário e plano da transação
                user_id = transaction.user_id

                if not user_id or not plan_type:
                    return WebhookVerificationResponse(
                        success=False,
                        message="Dados de usuário ou plano ausentes",
                        event_type=event_type
                    )

                # Criar ou atualizar a assinatura usando o serviço de assinatura
                subscription = await self.subscription_service.create_subscription(
                    user_id=user_id,
                    plan_type=plan_type,
                    payment_gateway=PaymentGateway.STRIPE,
                    gateway_subscription_id=event_data.get("subscription"),
                    amount=transaction.amount,
                    currency=transaction.currency
                )

                return WebhookVerificationResponse(
                    success=True,
                    message="Assinatura ativada com sucesso",
                    event_type=event_type,
                    subscription_id=str(subscription.id)
                )

            elif event_type == "customer.subscription.deleted":
                # Cancelar a assinatura
                subscription = await self.subscription_service.cancel_subscription(user_id)

                # Registrar que foi cancelada por webhook
                await self.transaction_repo.create(
                    user_id=user_id,
                    transaction_id=event_data.get("id", ""),
                    payment_gateway=PaymentGateway.STRIPE,
                    transaction_type=TransactionType.CANCELLATION,
                    amount=0,
                    currency="BRL",
                    status=TransactionStatus.COMPLETED,
                    metadata=event_data
                )

                return WebhookVerificationResponse(
                    success=True,
                    message="Assinatura cancelada com sucesso",
                    event_type=event_type,
                    subscription_id=str(
                        subscription.id) if subscription else None
                )

            # Outros tipos de evento
            return WebhookVerificationResponse(
                success=True,
                message=f"Evento {event_type} recebido e processado",
                event_type=event_type
            )

        except Exception as e:
            logger.error(f"Erro ao processar webhook do Stripe: {str(e)}")
            return WebhookVerificationResponse(
                success=False,
                message=f"Erro ao processar webhook: {str(e)}",
                event_type=event_type
            )
