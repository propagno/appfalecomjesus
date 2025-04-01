import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
from uuid import UUID

import stripe
from fastapi import HTTPException, status

from app.core.config import settings

logger = logging.getLogger(__name__)


class StripeService:
    """
    Serviço para integração com Stripe.

    Responsável por:
    - Criar sessões de checkout
    - Processar webhooks
    - Gerenciar assinaturas
    - Controlar pagamentos

    Attributes:
        stripe: Cliente do Stripe configurado com API key
    """

    def __init__(self):
        """
        Inicializa o serviço do Stripe.

        Configura API key e cliente.
        """
        stripe.api_key = settings.STRIPE_SECRET_KEY
        self.stripe = stripe

    async def create_checkout_session(
        self,
        user_id: UUID,
        plan_id: UUID,
        amount: int
    ) -> Dict:
        """
        Cria sessão de checkout para pagamento.

        Args:
            user_id: ID do usuário
            plan_id: ID do plano
            amount: Valor em centavos

        Returns:
            Dict com ID da sessão e URL

        Raises:
            HTTPException: Se erro na criação
        """
        try:
            # Cria sessão
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": "brl",
                        "unit_amount": amount,
                        "product_data": {
                            "name": "Assinatura Premium",
                            "description": "Acesso ilimitado ao FaleComJesus"
                        }
                    },
                    "quantity": 1
                }],
                mode="subscription",
                success_url=settings.STRIPE_SUCCESS_URL,
                cancel_url=settings.STRIPE_CANCEL_URL,
                metadata={
                    "user_id": str(user_id),
                    "plan_id": str(plan_id)
                }
            )

            return {
                "id": session.id,
                "url": session.url,
                "amount": amount,
                "status": "pending"
            }

        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao criar checkout no Stripe"
            )
        except Exception as e:
            logger.error(f"Error creating checkout: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao criar checkout"
            )

    async def verify_webhook_signature(
        self,
        payload: bytes,
        sig_header: str
    ) -> bool:
        """
        Verifica assinatura do webhook Stripe.

        Args:
            payload: Dados do webhook
            sig_header: Assinatura do Stripe

        Returns:
            True se assinatura válida

        Raises:
            HTTPException: Se assinatura inválida
        """
        try:
            stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET
            )
            return True
        except stripe.error.SignatureVerificationError:
            logger.error("Invalid webhook signature")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assinatura do webhook inválida"
            )
        except Exception as e:
            logger.error(f"Error verifying webhook: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao verificar webhook"
            )

    async def cancel_subscription(
        self,
        subscription_id: str
    ) -> None:
        """
        Cancela assinatura no Stripe.

        Args:
            subscription_id: ID da assinatura

        Raises:
            HTTPException: Se erro no cancelamento
        """
        try:
            stripe.Subscription.delete(subscription_id)
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao cancelar assinatura no Stripe"
            )
        except Exception as e:
            logger.error(f"Error canceling subscription: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao cancelar assinatura"
            )

    async def refund_payment(
        self,
        payment_intent_id: str
    ) -> None:
        """
        Processa reembolso de pagamento.

        Args:
            payment_intent_id: ID do pagamento

        Raises:
            HTTPException: Se erro no reembolso
        """
        try:
            stripe.Refund.create(payment_intent=payment_intent_id)
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao reembolsar pagamento no Stripe"
            )
        except Exception as e:
            logger.error(f"Error refunding payment: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao reembolsar"
            )

    async def get_payment_method(
        self,
        payment_method_id: str
    ) -> Optional[Dict]:
        """
        Retorna detalhes do método de pagamento.

        Args:
            payment_method_id: ID do método

        Returns:
            Dict com detalhes ou None

        Raises:
            HTTPException: Se erro na busca
        """
        try:
            payment_method = stripe.PaymentMethod.retrieve(payment_method_id)
            return {
                "id": payment_method.id,
                "type": payment_method.type,
                "card": {
                    "brand": payment_method.card.brand,
                    "last4": payment_method.card.last4,
                    "exp_month": payment_method.card.exp_month,
                    "exp_year": payment_method.card.exp_year
                }
            }
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao buscar método de pagamento no Stripe"
            )
        except Exception as e:
            logger.error(f"Error getting payment method: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao buscar método"
            )
