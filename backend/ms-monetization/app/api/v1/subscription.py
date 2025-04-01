from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import logging

from app.schemas import (
    SubscriptionStatusResponse,
    SubscriptionDB,
    SubscriptionPlanDB
)
from app.dependencies import (
    get_current_user,
    get_subscription_service,
    get_redis_client,
    get_subscription_plan_repository
)
from app.services.subscription_service import SubscriptionService
from app.repositories import SubscriptionPlanRepository
from app.infrastructure.redis_client import RedisClient

# Configurar logger
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/subscription-status", response_model=SubscriptionStatusResponse)
async def get_subscription_status(
    user_id: str = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(
        get_subscription_service),
    redis_client: RedisClient = Depends(get_redis_client)
):
    """
    Retorna o status da assinatura do usuário atual com detalhes.
    Usado pelo frontend para verificar o tipo de plano e benefícios.
    """
    try:
        # Verificar o limite de mensagens restantes no Redis
        remaining_messages = await redis_client.check_chat_limit(user_id)

        # Obter status completo da assinatura
        status = await subscription_service.get_subscription_status(
            user_id=user_id,
            remaining_messages=remaining_messages
        )

        return status
    except Exception as e:
        logger.error(f"Erro ao recuperar status da assinatura: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao recuperar status da assinatura"
        )


@router.post("/cancel", response_model=SubscriptionDB)
async def cancel_subscription(
    user_id: str = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(
        get_subscription_service)
):
    """
    Cancela a assinatura premium do usuário.
    A assinatura continua válida até o final do período pago,
    mas não será renovada automaticamente.
    """
    try:
        subscription = await subscription_service.cancel_subscription(user_id)

        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assinatura não encontrada"
            )

        return subscription
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao cancelar assinatura: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao cancelar assinatura"
        )


@router.get("/plans", response_model=List[SubscriptionPlanDB])
async def get_subscription_plans(
    active_only: bool = True,
    plan_repo: SubscriptionPlanRepository = Depends(
        get_subscription_plan_repository)
):
    """
    Retorna a lista de planos de assinatura disponíveis.
    Usado pelo frontend para exibir os planos e preços.
    """
    try:
        # Garantir que os planos padrão existam
        await plan_repo.seed_default_plans()

        # Retornar todos os planos
        plans = await plan_repo.get_all(active_only=active_only)
        return plans
    except Exception as e:
        logger.error(f"Erro ao listar planos de assinatura: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar planos de assinatura"
        )
