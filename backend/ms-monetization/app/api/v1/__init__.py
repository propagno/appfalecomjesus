from fastapi import APIRouter
from .subscription import router as subscription_router
from .ad_reward import router as ad_reward_router
from .payment import router as payment_router
from .chat_limit import router as chat_limit_router

api_router = APIRouter()

api_router.include_router(
    subscription_router, prefix="/subscription", tags=["subscription"])
api_router.include_router(ad_reward_router, prefix="/ads", tags=["ads"])
api_router.include_router(payment_router, prefix="/payment", tags=["payment"])
api_router.include_router(
    chat_limit_router, prefix="/chat", tags=["chat_limit"])
