from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.future import select
from typing import List, Optional, Dict
from datetime import datetime

from app.models import SubscriptionPlan


class SubscriptionPlanRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str, display_name: str, description: str,
                     price: float = 0.0, currency: str = "BRL",
                     duration_days: int = 30, benefits: Dict = None,
                     is_active: bool = True, trial_days: int = 0,
                     sort_order: int = 0) -> SubscriptionPlan:
        """Cria um novo plano de assinatura."""
        if benefits is None:
            benefits = {}

        plan = SubscriptionPlan(
            name=name,
            display_name=display_name,
            description=description,
            price=price,
            currency=currency,
            duration_days=duration_days,
            benefits=benefits,
            is_active=is_active,
            trial_days=trial_days,
            sort_order=sort_order,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.session.add(plan)
        await self.session.commit()
        await self.session.refresh(plan)
        return plan

    async def get_by_id(self, plan_id: int) -> Optional[SubscriptionPlan]:
        """Busca um plano pelo ID."""
        query = select(SubscriptionPlan).where(SubscriptionPlan.id == plan_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_name(self, name: str) -> Optional[SubscriptionPlan]:
        """Busca um plano pelo nome."""
        query = select(SubscriptionPlan).where(SubscriptionPlan.name == name)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_all(self, active_only: bool = True) -> List[SubscriptionPlan]:
        """Retorna todos os planos disponíveis."""
        query = select(SubscriptionPlan)

        if active_only:
            query = query.where(SubscriptionPlan.is_active == True)

        query = query.order_by(SubscriptionPlan.sort_order)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, plan_id: int, **kwargs) -> Optional[SubscriptionPlan]:
        """Atualiza um plano existente."""
        # Adicionar o timestamp de atualização
        kwargs["updated_at"] = datetime.utcnow()

        # Executar a atualização
        stmt = update(SubscriptionPlan).where(
            SubscriptionPlan.id == plan_id).values(**kwargs)
        await self.session.execute(stmt)

        # Buscar o plano atualizado
        await self.session.commit()
        return await self.get_by_id(plan_id)

    async def delete(self, plan_id: int) -> bool:
        """Exclui um plano do banco de dados."""
        stmt = delete(SubscriptionPlan).where(SubscriptionPlan.id == plan_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return True

    async def seed_default_plans(self) -> List[SubscriptionPlan]:
        """Cria os planos padrão caso não existam."""
        plans = []

        # Plano Gratuito
        free_plan = await self.get_by_name("free")
        if not free_plan:
            free_plan = await self.create(
                name="free",
                display_name="Gratuito",
                description="Acesso limitado às funcionalidades básicas.",
                price=0.0,
                benefits={
                    "chat_messages_per_day": 5,
                    "studies_per_month": 10,
                    "ad_free": False,
                    "premium_content": False
                },
                sort_order=1
            )
            plans.append(free_plan)

        # Plano Mensal
        monthly_plan = await self.get_by_name("monthly")
        if not monthly_plan:
            monthly_plan = await self.create(
                name="monthly",
                display_name="Premium Mensal",
                description="Acesso completo com pagamento mensal.",
                price=19.90,
                duration_days=30,
                benefits={
                    "chat_messages_per_day": -1,  # Ilimitado
                    "studies_per_month": -1,      # Ilimitado
                    "ad_free": True,
                    "premium_content": True
                },
                sort_order=2
            )
            plans.append(monthly_plan)

        # Plano Anual
        annual_plan = await self.get_by_name("annual")
        if not annual_plan:
            annual_plan = await self.create(
                name="annual",
                display_name="Premium Anual",
                description="Acesso completo com pagamento anual e desconto.",
                price=199.90,
                duration_days=365,
                benefits={
                    "chat_messages_per_day": -1,  # Ilimitado
                    "studies_per_month": -1,      # Ilimitado
                    "ad_free": True,
                    "premium_content": True
                },
                sort_order=3
            )
            plans.append(annual_plan)

        return plans
