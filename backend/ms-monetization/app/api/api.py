from fastapi import APIRouter
from app.api.routes import subscriptions, webhooks, payment, ad_rewards, chat_limits

api_router = APIRouter()

api_router.include_router(subscriptions.router,
                          prefix="/subscriptions", tags=["Subscriptions"])
api_router.include_router(
    webhooks.router, prefix="/webhooks", tags=["Webhooks"])
api_router.include_router(payment.router, prefix="/payment", tags=["Payment"])
api_router.include_router(
    ad_rewards.router, prefix="/ad-rewards", tags=["Ad Rewards"])
api_router.include_router(
    chat_limits.router, prefix="/chat-limits", tags=["chat-limits"])
