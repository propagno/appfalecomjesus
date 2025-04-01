from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime, timedelta

from app.models import AdReward


class AdRewardRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: str, reward_type: str, reward_value: int = 5,
                     ad_provider: str = "google", ad_id: Optional[str] = None,
                     ip_address: Optional[str] = None) -> AdReward:
        """Cria um novo registro de recompensa por anúncio assistido."""
        ad_reward = AdReward(
            user_id=user_id,
            ad_provider=ad_provider,
            ad_id=ad_id,
            reward_type=reward_type,
            reward_value=reward_value,
            status="completed",
            ip_address=ip_address,
            created_at=datetime.utcnow()
        )

        self.session.add(ad_reward)
        await self.session.commit()
        await self.session.refresh(ad_reward)
        return ad_reward

    async def get_by_id(self, ad_reward_id: int) -> Optional[AdReward]:
        """Busca uma recompensa pelo ID."""
        query = select(AdReward).where(AdReward.id == ad_reward_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_user_rewards_today(self, user_id: str) -> List[AdReward]:
        """Retorna todas as recompensas do usuário no dia atual."""
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)

        query = select(AdReward).where(
            (AdReward.user_id == user_id) &
            (AdReward.created_at >= today) &
            (AdReward.created_at < tomorrow)
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def count_user_rewards_today(self, user_id: str, reward_type: Optional[str] = None) -> int:
        """Conta quantas recompensas o usuário já recebeu hoje."""
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)

        query = select(func.count()).select_from(AdReward).where(
            (AdReward.user_id == user_id) &
            (AdReward.created_at >= today) &
            (AdReward.created_at < tomorrow)
        )

        if reward_type:
            query = query.where(AdReward.reward_type == reward_type)

        result = await self.session.execute(query)
        return result.scalar()

    async def get_total_rewards_value(self, user_id: str, reward_type: str) -> int:
        """Calcula o valor total de recompensas recebidas pelo usuário."""
        query = select(func.sum(AdReward.reward_value)).select_from(AdReward).where(
            (AdReward.user_id == user_id) &
            (AdReward.reward_type == reward_type)
        )

        result = await self.session.execute(query)
        return result.scalar() or 0

    async def get_user_rewards(self, user_id: str, limit: int = 10, offset: int = 0) -> List[AdReward]:
        """Retorna as recompensas do usuário paginadas."""
        query = select(AdReward).where(AdReward.user_id == user_id) \
            .order_by(AdReward.created_at.desc()) \
            .limit(limit).offset(offset)

        result = await self.session.execute(query)
        return result.scalars().all()
