import os
import sys
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.plan import Plan
from app.models.subscription import Subscription, SubscriptionStatus
from app.models.ad_reward import AdReward, AdType, RewardType

# Criar engine e sessão
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()


def seed_database():
    """Popula o banco de dados com dados iniciais"""
    try:
        # Criar planos
        plans = [
            Plan(
                id="11111111-1111-1111-1111-111111111111",
                name="Free",
                description="Acesso básico ao sistema",
                price_monthly=0,
                price_yearly=0,
                features={
                    "chat_messages_per_day": 5,
                    "study_days_per_month": 10,
                    "has_ads": True
                }
            ),
            Plan(
                id="22222222-2222-2222-2222-222222222222",
                name="Premium",
                description="Acesso ilimitado a todos os recursos",
                price_monthly=2990,
                price_yearly=29900,
                features={
                    "chat_messages_per_day": -1,
                    "study_days_per_month": -1,
                    "has_ads": False
                }
            )
        ]

        for plan in plans:
            db.add(plan)

        # Criar assinatura de exemplo
        subscription = Subscription(
            id="33333333-3333-3333-3333-333333333333",
            user_id="44444444-4444-4444-4444-444444444444",
            plan_id="22222222-2222-2222-2222-222222222222",
            status=SubscriptionStatus.ACTIVE,
            payment_gateway="Stripe",
            payment_id="pi_example",
            started_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        db.add(subscription)

        # Criar recompensa por anúncio de exemplo
        ad_reward = AdReward(
            id="55555555-5555-5555-5555-555555555555",
            user_id="44444444-4444-4444-4444-444444444444",
            ad_type=AdType.VIDEO,
            reward_type=RewardType.CHAT_MESSAGES,
            reward_value=5,
            watched_at=datetime.utcnow()
        )
        db.add(ad_reward)

        # Commit das alterações
        db.commit()
        print("Banco de dados populado com sucesso!")

    except Exception as e:
        print(f"Erro ao popular banco de dados: {str(e)}")
        db.rollback()
        sys.exit(1)

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
