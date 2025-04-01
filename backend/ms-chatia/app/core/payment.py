"""
Serviço de pagamentos do sistema FaleComJesus.

Este módulo implementa a integração com gateways de pagamento,
gerenciando assinaturas, cobranças e reembolsos.

Features:
    - Integração com Stripe
    - Integração com Hotmart
    - Assinaturas recorrentes
    - Pagamentos únicos
    - Reembolsos automáticos
    - Webhooks
"""

from typing import Dict, List, Optional, Union
import stripe
import logging
import json
import requests
from datetime import datetime, timedelta
from .config import settings
from .cache import cache
from .metrics import metrics
from .email import email

# Logger
logger = logging.getLogger(__name__)

# Configuração do Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


class PaymentManager:
    """
    Gerenciador de pagamentos e assinaturas.

    Features:
        - Múltiplos gateways
        - Assinaturas recorrentes
        - Webhooks
        - Métricas
        - Notificações

    Attributes:
        stripe_config: Config do Stripe
        hotmart_config: Config do Hotmart
        metrics: Métricas de pagamento
    """

    def __init__(
        self,
        stripe_key: Optional[str] = None,
        stripe_webhook: Optional[str] = None,
        hotmart_id: Optional[str] = None,
        hotmart_secret: Optional[str] = None
    ):
        """
        Inicializa o gerenciador de pagamentos.

        Args:
            stripe_key: API Key do Stripe
            stripe_webhook: Webhook Secret
            hotmart_id: Client ID Hotmart
            hotmart_secret: Client Secret
        """
        # Configuração Stripe
        self.stripe_config = {
            "api_key": stripe_key or settings.STRIPE_SECRET_KEY,
            "webhook_secret": stripe_webhook or settings.STRIPE_WEBHOOK_SECRET
        }

        # Configuração Hotmart
        self.hotmart_config = {
            "client_id": hotmart_id or settings.HOTMART_CLIENT_ID,
            "client_secret": hotmart_secret or settings.HOTMART_CLIENT_SECRET
        }

        logger.info("Gerenciador de pagamentos inicializado")

    async def create_checkout(
        self,
        user_id: str,
        plan_type: str,
        success_url: str,
        cancel_url: str,
        payment_method: str = "card",
        currency: str = "brl"
    ) -> Dict:
        """
        Cria sessão de checkout.

        Args:
            user_id: ID do usuário
            plan_type: Tipo do plano
            success_url: URL de sucesso
            cancel_url: URL de cancelamento
            payment_method: Método de pagamento
            currency: Moeda

        Returns:
            Dict: Dados do checkout

        Example:
            checkout = await payment.create_checkout(
                user_id="123",
                plan_type="premium_mensal",
                success_url="https://app.com/success",
                cancel_url="https://app.com/cancel"
            )
        """
        try:
            # Obtém preço do plano
            price_id = await self._get_plan_price(
                plan_type,
                currency
            )

            # Cria checkout Stripe
            session = stripe.checkout.Session.create(
                customer_email=user_id,
                payment_method_types=[payment_method],
                line_items=[{
                    "price": price_id,
                    "quantity": 1
                }],
                mode="subscription",
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    "user_id": user_id,
                    "plan_type": plan_type
                }
            )

            # Registra métricas
            metrics.track_payment(
                "checkout_created",
                plan_type=plan_type,
                gateway="stripe"
            )

            return {
                "id": session.id,
                "url": session.url
            }

        except stripe.error.StripeError as e:
            logger.error(f"Erro Stripe: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Erro ao criar checkout: {str(e)}")
            raise

    async def process_webhook(
        self,
        payload: bytes,
        signature: str,
        gateway: str = "stripe"
    ) -> Dict:
        """
        Processa webhook de pagamento.

        Args:
            payload: Dados do webhook
            signature: Assinatura
            gateway: Gateway de pagamento

        Returns:
            Dict: Resultado do processamento
        """
        try:
            if gateway == "stripe":
                return await self._process_stripe_webhook(
                    payload,
                    signature
                )
            elif gateway == "hotmart":
                return await self._process_hotmart_webhook(
                    payload,
                    signature
                )
            else:
                raise ValueError(f"Gateway inválido: {gateway}")

        except Exception as e:
            logger.error(f"Erro no webhook: {str(e)}")
            raise

    async def cancel_subscription(
        self,
        subscription_id: str,
        gateway: str = "stripe"
    ) -> bool:
        """
        Cancela assinatura.

        Args:
            subscription_id: ID da assinatura
            gateway: Gateway de pagamento

        Returns:
            bool: True se cancelada
        """
        try:
            if gateway == "stripe":
                # Cancela no Stripe
                stripe.Subscription.delete(subscription_id)

            elif gateway == "hotmart":
                # Cancela na Hotmart
                url = f"{settings.HOTMART_BASE_URL}/subscriptions/{subscription_id}/cancel"
                headers = await self._get_hotmart_headers()

                response = requests.post(url, headers=headers)
                response.raise_for_status()

            # Registra métricas
            metrics.track_payment(
                "subscription_canceled",
                gateway=gateway
            )

            # Notifica usuário
            await email.send_email(
                to_email=user_email,
                subject="Assinatura cancelada",
                template_name="subscription_canceled.html",
                template_data={}
            )

            return True

        except Exception as e:
            logger.error(f"Erro ao cancelar assinatura: {str(e)}")
            return False

    async def refund_payment(
        self,
        payment_id: str,
        amount: Optional[int] = None,
        reason: Optional[str] = None,
        gateway: str = "stripe"
    ) -> bool:
        """
        Realiza reembolso.

        Args:
            payment_id: ID do pagamento
            amount: Valor opcional
            reason: Motivo opcional
            gateway: Gateway de pagamento

        Returns:
            bool: True se reembolsado
        """
        try:
            if gateway == "stripe":
                # Reembolso Stripe
                stripe.Refund.create(
                    payment_intent=payment_id,
                    amount=amount,
                    reason=reason
                )

            elif gateway == "hotmart":
                # Reembolso Hotmart
                url = f"{settings.HOTMART_BASE_URL}/payments/{payment_id}/refund"
                headers = await self._get_hotmart_headers()

                data = {
                    "amount": amount,
                    "reason": reason
                }

                response = requests.post(
                    url,
                    headers=headers,
                    json=data
                )
                response.raise_for_status()

            # Registra métricas
            metrics.track_payment(
                "payment_refunded",
                amount=amount,
                gateway=gateway
            )

            # Notifica usuário
            await email.send_email(
                to_email=user_email,
                subject="Reembolso processado",
                template_name="refund_processed.html",
                template_data={
                    "amount": amount,
                    "reason": reason
                }
            )

            return True

        except Exception as e:
            logger.error(f"Erro ao realizar reembolso: {str(e)}")
            return False

    async def _process_stripe_webhook(
        self,
        payload: bytes,
        signature: str
    ) -> Dict:
        """
        Processa webhook do Stripe.

        Args:
            payload: Dados do webhook
            signature: Assinatura Stripe

        Returns:
            Dict: Resultado processado
        """
        try:
            # Verifica assinatura
            event = stripe.Webhook.construct_event(
                payload,
                signature,
                self.stripe_config["webhook_secret"]
            )

            # Processa evento
            if event.type == "checkout.session.completed":
                await self._handle_checkout_completed(event.data.object)

            elif event.type == "invoice.paid":
                await self._handle_invoice_paid(event.data.object)

            elif event.type == "invoice.payment_failed":
                await self._handle_payment_failed(event.data.object)

            # Registra métricas
            metrics.track_payment(
                "webhook_processed",
                event_type=event.type,
                gateway="stripe"
            )

            return {"status": "processed"}

        except stripe.error.SignatureVerificationError:
            logger.error("Assinatura Stripe inválida")
            raise

        except Exception as e:
            logger.error(f"Erro no webhook Stripe: {str(e)}")
            raise

    async def _process_hotmart_webhook(
        self,
        payload: bytes,
        signature: str
    ) -> Dict:
        """
        Processa webhook da Hotmart.

        Args:
            payload: Dados do webhook
            signature: Assinatura Hotmart

        Returns:
            Dict: Resultado processado
        """
        try:
            # Verifica assinatura
            if not self._verify_hotmart_signature(
                payload,
                signature
            ):
                raise ValueError("Assinatura Hotmart inválida")

            # Parse do payload
            data = json.loads(payload)

            # Processa evento
            if data["event"] == "PURCHASE_APPROVED":
                await self._handle_purchase_approved(data)

            elif data["event"] == "PURCHASE_CANCELED":
                await self._handle_purchase_canceled(data)

            elif data["event"] == "SUBSCRIPTION_CANCELED":
                await self._handle_subscription_canceled(data)

            # Registra métricas
            metrics.track_payment(
                "webhook_processed",
                event_type=data["event"],
                gateway="hotmart"
            )

            return {"status": "processed"}

        except Exception as e:
            logger.error(f"Erro no webhook Hotmart: {str(e)}")
            raise

    async def _get_plan_price(
        self,
        plan_type: str,
        currency: str
    ) -> str:
        """
        Obtém ID do preço do plano.

        Args:
            plan_type: Tipo do plano
            currency: Moeda

        Returns:
            str: ID do preço
        """
        # Cache de preços
        cache_key = f"price:{plan_type}:{currency}"
        price_id = await cache.get(cache_key)

        if price_id:
            return price_id

        # Busca preço no Stripe
        prices = stripe.Price.list(
            lookup_keys=[plan_type],
            active=True,
            currency=currency
        )

        if not prices.data:
            raise ValueError(f"Preço não encontrado: {plan_type}")

        # Cache por 1 hora
        await cache.set(
            cache_key,
            prices.data[0].id,
            expire=3600
        )

        return prices.data[0].id

    async def _get_hotmart_headers(self) -> Dict:
        """
        Gera headers para API Hotmart.

        Returns:
            Dict: Headers com token
        """
        # Cache do token
        cache_key = "hotmart:token"
        token = await cache.get(cache_key)

        if not token:
            # Gera novo token
            url = f"{settings.HOTMART_BASE_URL}/oauth/token"
            data = {
                "grant_type": "client_credentials",
                "client_id": self.hotmart_config["client_id"],
                "client_secret": self.hotmart_config["client_secret"]
            }

            response = requests.post(url, data=data)
            response.raise_for_status()

            token = response.json()["access_token"]

            # Cache por 1 hora
            await cache.set(
                cache_key,
                token,
                expire=3600
            )

        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }


# Instância global de pagamentos
payment = PaymentManager()
