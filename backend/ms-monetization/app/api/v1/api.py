from fastapi import APIRouter
from app.api.v1.endpoints import plans, subscription, checkout, webhook, ad_rewards

api_router = APIRouter()

# Rotas de planos
api_router.include_router(
    plans.router,
    prefix="/plans",
    tags=["plans"]
)

# Rotas de assinatura
api_router.include_router(
    subscription.router,
    prefix="/subscription",
    tags=["subscription"]
)

# Rotas de checkout
api_router.include_router(
    checkout.router,
    prefix="/checkout",
    tags=["checkout"]
)

# Rotas de webhook
api_router.include_router(
    webhook.router,
    prefix="/webhook",
    tags=["webhook"]
)

# Rotas de recompensas por anúncios
api_router.include_router(
    ad_rewards.router,
    prefix="/ad-rewards",
    tags=["ad-rewards"]
)
