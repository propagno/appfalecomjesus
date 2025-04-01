from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.future import select
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from app.models import Subscription, SubscriptionStatus, SubscriptionPlan as SubscriptionPlanEnum


class SubscriptionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: str, plan_type: str, payment_gateway: str = "none",
                     gateway_subscription_id: Optional[str] = None,
                     amount: float = 0.0, currency: str = "BRL") -> Subscription:
        """Cria uma nova assinatura para o usuário."""

        # Definir datas com base no tipo de plano
        now = datetime.utcnow()
        next_payment_date = None

        if plan_type == SubscriptionPlanEnum.MONTHLY:
            next_payment_date = now + timedelta(days=30)
        elif plan_type == SubscriptionPlanEnum.ANNUAL:
            next_payment_date = now + timedelta(days=365)

        subscription = Subscription(
            user_id=user_id,
            plan_type=plan_type,
            status=SubscriptionStatus.ACTIVE,
            payment_gateway=payment_gateway,
            gateway_subscription_id=gateway_subscription_id,
            last_payment_date=now if plan_type != SubscriptionPlanEnum.FREE else None,
            next_payment_date=next_payment_date,
            amount=amount,
            currency=currency,
            created_at=now,
            updated_at=now
        )

        self.session.add(subscription)
        await self.session.commit()
        await self.session.refresh(subscription)
        return subscription

    async def get_by_user_id(self, user_id: str) -> Optional[Subscription]:
        """Busca a assinatura de um usuário pelo ID."""
        query = select(Subscription).where(Subscription.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_id(self, subscription_id: int) -> Optional[Subscription]:
        """Busca uma assinatura pelo ID."""
        query = select(Subscription).where(Subscription.id == subscription_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def update(self, subscription_id: int, **kwargs) -> Optional[Subscription]:
        """Atualiza uma assinatura existente."""
        # Adicionar o timestamp de atualização
        kwargs["updated_at"] = datetime.utcnow()

        # Executar a atualização
        stmt = update(Subscription).where(
            Subscription.id == subscription_id).values(**kwargs)
        await self.session.execute(stmt)

        # Buscar a assinatura atualizada
        await self.session.commit()
        return await self.get_by_id(subscription_id)

    async def update_by_user_id(self, user_id: str, **kwargs) -> Optional[Subscription]:
        """Atualiza a assinatura de um usuário pelo ID."""
        subscription = await self.get_by_user_id(user_id)
        if not subscription:
            return None

        return await self.update(subscription.id, **kwargs)

    async def cancel_subscription(self, user_id: str) -> Optional[Subscription]:
        """Cancela a assinatura de um usuário."""
        subscription = await self.get_by_user_id(user_id)
        if not subscription:
            return None

        now = datetime.utcnow()
        return await self.update(
            subscription.id,
            status=SubscriptionStatus.CANCELED,
            is_auto_renew=False,
            canceled_at=now
        )

    async def get_active_subscriptions(self) -> List[Subscription]:
        """Retorna todas as assinaturas ativas."""
        query = select(Subscription).where(
            Subscription.status == SubscriptionStatus.ACTIVE)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_expired_subscriptions(self) -> List[Subscription]:
        """Retorna todas as assinaturas expiradas que precisam ser renovadas ou canceladas."""
        now = datetime.utcnow()
        query = select(Subscription).where(
            (Subscription.status == SubscriptionStatus.ACTIVE) &
            (Subscription.next_payment_date < now) &
            (Subscription.plan_type != SubscriptionPlanEnum.FREE)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete(self, subscription_id: int) -> bool:
        """Exclui uma assinatura do banco de dados."""
        stmt = delete(Subscription).where(Subscription.id == subscription_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return True
