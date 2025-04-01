import logging
import stripe
import hmac
import hashlib
import json
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.services.subscription_service import SubscriptionService
from app.services.auth_service import AuthService
from app.models.subscription import SubscriptionStatus, PaymentGateway
from typing import Tuple, Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger("webhook_service")


class WebhookService:
    """
    Serviço para processar webhooks de pagamento de Stripe e Hotmart
    """

    @staticmethod
    async def handle_stripe_webhook(
        db: Session,
        payload: bytes,
        signature: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Processa webhooks do Stripe

        Args:
            db: Sessão do banco de dados
            payload: O payload do webhook
            signature: A assinatura do webhook

        Returns:
            tuple: (sucesso, mensagem de erro)
        """
        try:
            # Verificar assinatura com chave secreta do webhook
            event = stripe.Webhook.construct_event(
                payload, signature, settings.STRIPE_WEBHOOK_SECRET
            )

            logger.info(f"Webhook Stripe recebido: {event.type}")

            # Processar os diferentes tipos de eventos
            if event.type == 'checkout.session.completed':
                return await WebhookService._handle_checkout_completed(db, event.data.object)

            elif event.type == 'customer.subscription.updated':
                return await WebhookService._handle_subscription_updated(db, event.data.object)

            elif event.type == 'customer.subscription.deleted':
                return await WebhookService._handle_subscription_canceled(db, event.data.object)

            elif event.type == 'invoice.payment_failed':
                return await WebhookService._handle_payment_failed(db, event.data.object)

            # Evento não tratado
            logger.warning(f"Evento Stripe não processado: {event.type}")
            return True, None

        except stripe.error.SignatureVerificationError:
            logger.error("Assinatura do webhook inválida!")
            return False, "Assinatura do webhook inválida!"

        except Exception as e:
            logger.exception(f"Erro ao processar webhook do Stripe: {str(e)}")
            return False, f"Erro interno: {str(e)}"

    @staticmethod
    async def handle_hotmart_webhook(
        db: Session,
        payload: Dict[str, Any]
    ) -> Tuple[bool, Optional[str]]:
        """
        Processa webhooks do Hotmart

        Args:
            db: Sessão do banco de dados
            payload: O payload do webhook

        Returns:
            tuple: (sucesso, mensagem de erro)
        """
        try:
            # Validar o payload básico
            if not payload or 'data' not in payload or 'event' not in payload:
                logger.error("Payload Hotmart inválido")
                return False, "Payload inválido"

            event_type = payload.get('event')
            data = payload.get('data', {})

            logger.info(f"Webhook Hotmart recebido: {event_type}")

            # Validar a autenticidade (hotmart tem diversos métodos de autenticação)
            # Este é um exemplo, mas pode precisar ser adaptado conforme documentação da Hotmart
            if not WebhookService._validate_hotmart_webhook(payload):
                logger.error("Autenticação do webhook Hotmart falhou")
                return False, "Falha na autenticação do webhook"

            # Processar os diferentes tipos de eventos
            if event_type == 'PURCHASE_APPROVED':
                return await WebhookService._handle_hotmart_purchase_approved(db, data)

            elif event_type == 'PURCHASE_CANCELED' or event_type == 'PURCHASE_REFUNDED':
                return await WebhookService._handle_hotmart_purchase_canceled(db, data)

            elif event_type == 'SUBSCRIPTION_CANCELED':
                return await WebhookService._handle_hotmart_subscription_canceled(db, data)

            elif event_type == 'SUBSCRIPTION_REACTIVATED':
                return await WebhookService._handle_hotmart_subscription_reactivated(db, data)

            # Evento não tratado
            logger.warning(f"Evento Hotmart não processado: {event_type}")
            return True, None

        except Exception as e:
            logger.exception(f"Erro ao processar webhook do Hotmart: {str(e)}")
            return False, f"Erro interno: {str(e)}"

    @staticmethod
    async def _handle_checkout_completed(db: Session, checkout_session: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Processa evento de checkout concluído do Stripe
        """
        try:
            # Extrair dados do checkout
            user_id = checkout_session.get('client_reference_id')
            subscription_id = checkout_session.get('subscription')

            if not user_id:
                logger.error(
                    "client_reference_id (user_id) não encontrado no checkout")
                return False, "User ID não encontrado"

            # Verificar se é uma assinatura ou pagamento único
            if subscription_id:
                # É uma assinatura - obter detalhes da assinatura
                subscription = stripe.Subscription.retrieve(subscription_id)

                # Obter duração do plano
                plan_interval = subscription.items.data[0].plan.interval
                plan_interval_count = subscription.items.data[0].plan.interval_count

                # Calcular data de expiração
                expires_at = WebhookService._calculate_expiration_date(
                    plan_interval, plan_interval_count)

                # Criar ou atualizar assinatura no banco de dados
                subscription_service = SubscriptionService(db)
                await subscription_service.create_or_update_subscription(
                    user_id=user_id,
                    payment_gateway=PaymentGateway.STRIPE,
                    external_id=subscription_id,
                    status=SubscriptionStatus.ACTIVE,
                    expires_at=expires_at
                )

                # Atualizar assinatura no MS-Auth
                await AuthService.update_user_subscription(
                    user_id=user_id,
                    subscription_data={
                        "subscription_type": "premium",
                        "status": "active",
                        "payment_gateway": "stripe",
                        "expiration_date": expires_at.isoformat(),
                        "last_payment_date": datetime.utcnow().isoformat()
                    }
                )

                logger.info(
                    f"Assinatura criada/atualizada para usuário {user_id}")
                return True, None
            else:
                # Pagamento único
                logger.info(
                    f"Pagamento único processado para usuário {user_id}")
                return True, None

        except Exception as e:
            logger.exception(f"Erro ao processar checkout concluído: {str(e)}")
            return False, f"Erro ao processar checkout: {str(e)}"

    @staticmethod
    async def _handle_subscription_updated(db: Session, subscription_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Processa evento de atualização de assinatura do Stripe
        """
        try:
            subscription_id = subscription_data.get('id')
            status = subscription_data.get('status')

            # Mapear status do Stripe para nosso modelo
            if status == 'active':
                new_status = SubscriptionStatus.ACTIVE
                auth_status = "active"
            elif status == 'past_due':
                new_status = SubscriptionStatus.PAST_DUE
                auth_status = "past_due"
            elif status == 'canceled':
                new_status = SubscriptionStatus.CANCELED
                auth_status = "cancelled"
            else:
                new_status = SubscriptionStatus.INACTIVE
                auth_status = "inactive"

            # Atualizar assinatura no banco de dados
            subscription_service = SubscriptionService(db)
            subscription = await subscription_service.get_subscription_by_external_id(
                external_id=subscription_id,
                payment_gateway=PaymentGateway.STRIPE
            )

            if not subscription:
                logger.warning(
                    f"Assinatura {subscription_id} não encontrada para atualização")
                return False, "Assinatura não encontrada"

            # Atualizar status
            await subscription_service.update_subscription_status(
                subscription_id=subscription.id,
                status=new_status
            )

            # Atualizar assinatura no MS-Auth
            await AuthService.update_user_subscription(
                user_id=subscription.user_id,
                subscription_data={
                    "subscription_type": "premium",
                    "status": auth_status,
                    "payment_gateway": "stripe"
                }
            )

            logger.info(
                f"Assinatura {subscription_id} atualizada para status {new_status}")
            return True, None

        except Exception as e:
            logger.exception(
                f"Erro ao processar atualização de assinatura: {str(e)}")
            return False, f"Erro ao atualizar assinatura: {str(e)}"

    @staticmethod
    async def _handle_subscription_canceled(db: Session, subscription_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Processa evento de cancelamento de assinatura do Stripe
        """
        try:
            subscription_id = subscription_data.get('id')

            # Atualizar assinatura no banco de dados
            subscription_service = SubscriptionService(db)
            subscription = await subscription_service.get_subscription_by_external_id(
                external_id=subscription_id,
                payment_gateway=PaymentGateway.STRIPE
            )

            if not subscription:
                logger.warning(
                    f"Assinatura {subscription_id} não encontrada para cancelamento")
                return False, "Assinatura não encontrada"

            # Atualizar status
            await subscription_service.update_subscription_status(
                subscription_id=subscription.id,
                status=SubscriptionStatus.CANCELED
            )

            # Atualizar assinatura no MS-Auth
            await AuthService.update_user_subscription(
                user_id=subscription.user_id,
                subscription_data={
                    "subscription_type": "free",
                    "status": "cancelled",
                    "payment_gateway": "stripe"
                }
            )

            logger.info(f"Assinatura {subscription_id} cancelada")
            return True, None

        except Exception as e:
            logger.exception(
                f"Erro ao processar cancelamento de assinatura: {str(e)}")
            return False, f"Erro ao cancelar assinatura: {str(e)}"

    @staticmethod
    async def _handle_payment_failed(db: Session, invoice_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Processa evento de falha de pagamento do Stripe
        """
        try:
            subscription_id = invoice_data.get('subscription')

            if subscription_id:
                # Atualizar assinatura no banco de dados
                subscription_service = SubscriptionService(db)
                subscription = await subscription_service.get_subscription_by_external_id(
                    external_id=subscription_id,
                    payment_gateway=PaymentGateway.STRIPE
                )

                if not subscription:
                    logger.warning(
                        f"Assinatura {subscription_id} não encontrada para atualizar status de pagamento")
                    return False, "Assinatura não encontrada"

                # Atualizar status
                await subscription_service.update_subscription_status(
                    subscription_id=subscription.id,
                    status=SubscriptionStatus.PAST_DUE
                )

                logger.info(
                    f"Assinatura {subscription_id} marcada como pagamento pendente")

            return True, None

        except Exception as e:
            logger.exception(f"Erro ao processar falha de pagamento: {str(e)}")
            return False, f"Erro ao processar falha de pagamento: {str(e)}"

    @staticmethod
    async def _handle_hotmart_purchase_approved(db: Session, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Processa evento de compra aprovada no Hotmart
        """
        try:
            # Extrair dados necessários
            buyer_email = data.get('buyer', {}).get('email')
            subscription_id = data.get('subscription', {}).get('code')
            product_id = data.get('product', {}).get('id')
            purchase_code = data.get('purchase', {}).get('code')

            if not buyer_email:
                logger.error(
                    "Email do comprador não encontrado no webhook Hotmart")
                return False, "Email do comprador não encontrado"

            # Recuperar o user_id do MS-Auth usando o email (via API)
            user_id = await WebhookService._get_user_id_by_email(buyer_email)

            if not user_id:
                logger.error(f"Usuário com email {buyer_email} não encontrado")
                return False, f"Usuário não encontrado para email: {buyer_email}"

            # Verificar se é assinatura ou produto único
            if subscription_id:
                # É uma assinatura - obter detalhes e calcular vencimento
                plan_data = data.get('subscription', {})
                plan_status = plan_data.get('status')

                # Calcular data de expiração com base no plano Hotmart
                expires_at = WebhookService._calculate_hotmart_expiration(
                    plan_data)

                # Converter status do Hotmart para nosso modelo
                status = SubscriptionStatus.ACTIVE if plan_status == 'ACTIVE' else SubscriptionStatus.INACTIVE
                auth_status = "active" if plan_status == 'ACTIVE' else "inactive"

                # Criar ou atualizar assinatura
                subscription_service = SubscriptionService(db)
                await subscription_service.create_or_update_subscription(
                    user_id=user_id,
                    payment_gateway=PaymentGateway.HOTMART,
                    external_id=subscription_id,
                    status=status,
                    expires_at=expires_at
                )

                # Atualizar assinatura no MS-Auth
                await AuthService.update_user_subscription(
                    user_id=user_id,
                    subscription_data={
                        "subscription_type": "premium",
                        "status": auth_status,
                        "payment_gateway": "hotmart",
                        "expiration_date": expires_at.isoformat(),
                        "last_payment_date": datetime.utcnow().isoformat()
                    }
                )

                logger.info(
                    f"Assinatura Hotmart criada/atualizada para usuário {user_id}")
            else:
                # É um produto de pagamento único
                # Implementar se necessário
                logger.info(
                    f"Compra única Hotmart processada para usuário {user_id}")

            return True, None

        except Exception as e:
            logger.exception(
                f"Erro ao processar compra aprovada Hotmart: {str(e)}")
            return False, f"Erro ao processar compra: {str(e)}"

    @staticmethod
    async def _handle_hotmart_purchase_canceled(db: Session, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Processa evento de compra cancelada ou reembolsada no Hotmart
        """
        try:
            subscription_id = data.get('subscription', {}).get('code')

            if subscription_id:
                subscription_service = SubscriptionService(db)
                subscription = await subscription_service.get_subscription_by_external_id(
                    external_id=subscription_id,
                    payment_gateway=PaymentGateway.HOTMART
                )

                if not subscription:
                    logger.warning(
                        f"Assinatura Hotmart {subscription_id} não encontrada para cancelamento")
                    return False, "Assinatura não encontrada"

                # Atualizar status
                await subscription_service.update_subscription_status(
                    subscription_id=subscription.id,
                    status=SubscriptionStatus.CANCELED
                )

                logger.info(
                    f"Assinatura Hotmart {subscription_id} cancelada ou reembolsada")

            return True, None

        except Exception as e:
            logger.exception(
                f"Erro ao processar cancelamento de compra Hotmart: {str(e)}")
            return False, f"Erro ao processar cancelamento: {str(e)}"

    @staticmethod
    async def _handle_hotmart_subscription_canceled(db: Session, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Processa evento de cancelamento de assinatura no Hotmart
        """
        try:
            subscription_id = data.get('subscription', {}).get('code')

            if subscription_id:
                subscription_service = SubscriptionService(db)
                subscription = await subscription_service.get_subscription_by_external_id(
                    external_id=subscription_id,
                    payment_gateway=PaymentGateway.HOTMART
                )

                if not subscription:
                    logger.warning(
                        f"Assinatura Hotmart {subscription_id} não encontrada para cancelamento")
                    return False, "Assinatura não encontrada"

                # Atualizar status
                await subscription_service.update_subscription_status(
                    subscription_id=subscription.id,
                    status=SubscriptionStatus.CANCELED
                )

                logger.info(f"Assinatura Hotmart {subscription_id} cancelada")

            return True, None

        except Exception as e:
            logger.exception(
                f"Erro ao processar cancelamento de assinatura Hotmart: {str(e)}")
            return False, f"Erro ao processar cancelamento: {str(e)}"

    @staticmethod
    async def _handle_hotmart_subscription_reactivated(db: Session, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Processa evento de reativação de assinatura no Hotmart
        """
        try:
            subscription_id = data.get('subscription', {}).get('code')

            if subscription_id:
                subscription_service = SubscriptionService(db)
                subscription = await subscription_service.get_subscription_by_external_id(
                    external_id=subscription_id,
                    payment_gateway=PaymentGateway.HOTMART
                )

                if not subscription:
                    logger.warning(
                        f"Assinatura Hotmart {subscription_id} não encontrada para reativação")
                    return False, "Assinatura não encontrada"

                # Calcular nova data de expiração com base nos dados recebidos
                plan_data = data.get('subscription', {})
                expires_at = WebhookService._calculate_hotmart_expiration(
                    plan_data)

                # Atualizar status
                await subscription_service.update_subscription(
                    subscription_id=subscription.id,
                    status=SubscriptionStatus.ACTIVE,
                    expires_at=expires_at
                )

                logger.info(f"Assinatura Hotmart {subscription_id} reativada")

            return True, None

        except Exception as e:
            logger.exception(
                f"Erro ao processar reativação de assinatura Hotmart: {str(e)}")
            return False, f"Erro ao processar reativação: {str(e)}"

    @staticmethod
    def _calculate_expiration_date(interval: str, interval_count: int) -> datetime:
        """
        Calcula a data de expiração com base no intervalo do plano
        """
        now = datetime.utcnow()

        if interval == 'day':
            return now + timedelta(days=interval_count)
        elif interval == 'week':
            return now + timedelta(weeks=interval_count)
        elif interval == 'month':
            # Aproximação para meses (30 dias)
            return now + timedelta(days=30 * interval_count)
        elif interval == 'year':
            # Aproximação para anos (365 dias)
            return now + timedelta(days=365 * interval_count)
        else:
            # Padrão para 1 mês
            return now + timedelta(days=30)

    @staticmethod
    def _calculate_hotmart_expiration(plan_data: Dict[str, Any]) -> datetime:
        """
        Calcula a data de expiração para planos do Hotmart
        """
        # Hotmart pode fornecer esta data diretamente no webhook
        next_charge = plan_data.get('next_charge')
        if next_charge:
            # Converter string para datetime se necessário
            if isinstance(next_charge, str):
                try:
                    return datetime.fromisoformat(next_charge.replace('Z', '+00:00'))
                except (ValueError, TypeError):
                    pass

        # Fallback: calcular com base na recorrência
        now = datetime.utcnow()
        # Na Hotmart, o padrão é mensal se não houver outras informações
        return now + timedelta(days=30)

    @staticmethod
    def _validate_hotmart_webhook(payload: Dict[str, Any]) -> bool:
        """
        Valida a autenticidade do webhook do Hotmart
        Nota: implementar conforme documentação específica da Hotmart
        """
        # Versão simplificada (implementar verificação real conforme Hotmart)
        # A Hotmart geralmente fornece um token ou hash para validação

        # Exemplo simples - deve ser adaptado à documentação real da Hotmart
        if settings.HOTMART_VALIDATE_WEBHOOK:
            # Verificar algum token ou hash
            return True

        # Se não estiver validando em ambiente de desenvolvimento
        return True

    @staticmethod
    async def _get_user_id_by_email(email: str) -> Optional[str]:
        """
        Obtém o user_id do MS-Auth usando o email do usuário
        """
        # Usar o AuthService para buscar o usuário
        user_data = await AuthService.get_user_by_email(email)

        if user_data and "id" in user_data:
            return user_data["id"]

        logger.warning(f"Usuário com email {email} não encontrado no MS-Auth")
        return None
