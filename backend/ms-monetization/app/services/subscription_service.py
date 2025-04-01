from typing import Optional, Dict, List
from datetime import datetime, timedelta
import logging

from app.models import Subscription, SubscriptionPlan, SubscriptionStatus, SubscriptionPlan as SubscriptionPlanEnum
from app.repositories import SubscriptionRepository, SubscriptionPlanRepository
from app.schemas import SubscriptionStatusResponse
from app.services.redis_client import RedisClient

# Configurar logger
logger = logging.getLogger(__name__)


class SubscriptionService:
    def __init__(self, subscription_repo: SubscriptionRepository, plan_repo: SubscriptionPlanRepository, redis_client: RedisClient):
        self.subscription_repo = subscription_repo
        self.plan_repo = plan_repo
        self.redis_client = redis_client

    async def get_user_subscription(self, user_id: str) -> Optional[Subscription]:
        """Retorna a assinatura atual do usuário."""
        return await self.subscription_repo.get_by_user_id(user_id)

    async def create_subscription(self, user_id: str, plan_type: str,
                                  payment_gateway: str = "none",
                                  gateway_subscription_id: Optional[str] = None,
                                  amount: float = 0.0,
                                  currency: str = "BRL") -> Subscription:
        """Cria uma nova assinatura para o usuário."""
        # Verificar se já existe uma assinatura para este usuário
        existing = await self.subscription_repo.get_by_user_id(user_id)

        if existing:
            # Se já existe, atualizamos para o novo plano
            now = datetime.utcnow()
            next_payment_date = None

            if plan_type == SubscriptionPlanEnum.MONTHLY:
                next_payment_date = now + timedelta(days=30)
            elif plan_type == SubscriptionPlanEnum.ANNUAL:
                next_payment_date = now + timedelta(days=365)

            # Atualizar assinatura no banco de dados
            subscription = await self.subscription_repo.update(
                existing.id,
                plan_type=plan_type,
                status=SubscriptionStatus.ACTIVE,
                payment_gateway=payment_gateway,
                gateway_subscription_id=gateway_subscription_id,
                last_payment_date=now,
                next_payment_date=next_payment_date,
                amount=amount,
                currency=currency,
                is_auto_renew=True,
                canceled_at=None  # Limpar data de cancelamento se houver
            )

            # Se for plano premium, limpar qualquer limite de mensagens
            if plan_type != SubscriptionPlanEnum.FREE:
                # Remover limites de chat no Redis
                chat_key = f"chat_limit:{user_id}"
                await self.redis_client.delete(chat_key)

            return subscription
        else:
            # Se não existe, criamos uma nova
            return await self.subscription_repo.create(
                user_id=user_id,
                plan_type=plan_type,
                payment_gateway=payment_gateway,
                gateway_subscription_id=gateway_subscription_id,
                amount=amount,
                currency=currency
            )

    async def cancel_subscription(self, user_id: str) -> Optional[Subscription]:
        """Cancela a assinatura do usuário."""
        return await self.subscription_repo.cancel_subscription(user_id)

    async def get_subscription_status(self, user_id: str) -> SubscriptionStatusResponse:
        """Retorna o status da assinatura e os benefícios para o frontend."""
        # Buscar assinatura atual do usuário
        subscription = await self.subscription_repo.get_by_user_id(user_id)

        # Se não tiver assinatura, criar uma gratuita automaticamente
        if not subscription:
            logger.info(
                f"Criando assinatura gratuita para o usuário {user_id}")
            subscription = await self.subscription_repo.create(
                user_id=user_id,
                plan_type=SubscriptionPlanEnum.FREE
            )

        # Determinar se é premium baseado no tipo de plano
        is_premium = subscription.plan_type != SubscriptionPlanEnum.FREE

        # Buscar o plano completo para obter os benefícios
        plan = await self.plan_repo.get_by_name(subscription.plan_type)
        if not plan:
            # Se o plano não existe mais, criar planos padrão e usar o gratuito
            await self.plan_repo.seed_default_plans()
            plan = await self.plan_repo.get_by_name(SubscriptionPlanEnum.FREE)

        # Obter o número de mensagens restantes do Redis
        remaining_messages = None
        if not is_premium:
            chat_key = f"chat_limit:{user_id}"
            remaining_messages = await self.redis_client.get(chat_key)

            # Se não existir ainda no Redis, definir com o limite diário padrão
            if remaining_messages is None:
                chat_messages_per_day = plan.benefits.get(
                    "chat_messages_per_day", 5) if plan else 5

                # Definir até a meia-noite
                midnight = datetime.utcnow().replace(hour=23, minute=59, second=59)
                seconds_until_midnight = int(
                    (midnight - datetime.utcnow()).total_seconds())

                await self.redis_client.set(
                    chat_key,
                    chat_messages_per_day,
                    expire=seconds_until_midnight
                )
                remaining_messages = chat_messages_per_day

        # Criar o objeto de resposta
        status_response = SubscriptionStatusResponse(
            plan_type=subscription.plan_type,
            status=subscription.status,
            is_premium=is_premium,
            expiration_date=subscription.next_payment_date,
            features=plan.benefits if plan else {},
            # Definir limite de mensagens com base no plano
            chat_messages_per_day=plan.benefits.get(
                "chat_messages_per_day", 5) if plan else 5,
            # Incluir o número de mensagens restantes
            remaining_chat_messages=int(
                remaining_messages) if remaining_messages else None
        )

        return status_response

    async def check_expired_subscriptions(self) -> List[Subscription]:
        """Verifica e atualiza assinaturas expiradas."""
        expired = await self.subscription_repo.get_expired_subscriptions()
        updated = []

        for subscription in expired:
            if not subscription.is_auto_renew:
                # Se não tem renovação automática, marcar como inativo
                await self.subscription_repo.update(
                    subscription.id,
                    status=SubscriptionStatus.INACTIVE
                )
                logger.info(
                    f"Assinatura {subscription.id} marcada como inativa devido a não renovação automática")
            else:
                # Aqui seria o lugar para tentar renovação automática
                # Este é apenas um placeholder para lógica futura
                logger.info(
                    f"Assinatura {subscription.id} expirada, pendente de renovação automática")

            updated.append(subscription)

        return updated

    async def seed_free_plan_for_all_users(self, user_ids: List[str]) -> int:
        """Cria plano free para todos os usuários que ainda não têm assinatura."""
        count = 0

        for user_id in user_ids:
            existing = await self.subscription_repo.get_by_user_id(user_id)
            if not existing:
                await self.subscription_repo.create(
                    user_id=user_id,
                    plan_type=SubscriptionPlanEnum.FREE
                )
                count += 1

        return count

    async def decrement_chat_messages_limit(self, user_id: str) -> int:
        """
        Decrementa o contador de mensagens de chat disponíveis para usuários Free.
        Retorna o número de mensagens restantes.
        """
        subscription = await self.subscription_repo.get_by_user_id(user_id)

        # Se for premium, não tem limite
        if subscription and subscription.plan_type != SubscriptionPlanEnum.FREE:
            return -1  # -1 significa ilimitado

        # Decrementar o contador no Redis
        chat_key = f"chat_limit:{user_id}"
        remaining = await self.redis_client.decrement(chat_key)

        # Se menor que zero, resetar para zero
        if remaining < 0:
            await self.redis_client.set(chat_key, 0)
            return 0

        return remaining
