from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.api.deps import get_subscription_service, get_current_user_id, get_user_by_id
from app.schemas.subscription import SubscriptionResponse, SubscriptionCreate, SubscriptionUpdate
from app.services.subscription_service import SubscriptionService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/",
    response_model=SubscriptionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova assinatura",
    description="""
    Cria uma nova assinatura Premium para o usuário autenticado.
    
    Este endpoint é usado quando o usuário faz upgrade de plano, seja
    através da integração direta com o serviço ou via webhook de pagamento.
    A assinatura pode ter diferentes tipos de plano e gateways de pagamento.
    """,
    responses={
        201: {
            "description": "Assinatura criada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": "f8a5df6e-d182-4f3c-b8e7-1c02cd9f99a4",
                        "user_id": "5eb7cf5a-0742-42b8-a40c-fb85f3b337aa",
                        "plan_type": "PREMIUM",
                        "status": "ACTIVE",
                        "payment_gateway": "STRIPE",
                        "last_payment_date": "2023-03-29T12:34:56.123Z",
                        "next_payment_date": "2023-04-29T12:34:56.123Z",
                        "expires_at": "2023-04-29T12:34:56.123Z",
                        "created_at": "2023-03-29T12:34:56.123Z"
                    }
                }
            }
        },
        404: {
            "description": "Usuário não encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Usuário não encontrado"
                    }
                }
            }
        }
    }
)
async def create_subscription(
    subscription: SubscriptionCreate,
    user_id: str = Depends(get_current_user_id),
    subscription_service: SubscriptionService = Depends(
        get_subscription_service)
):
    """
    Cria uma nova assinatura para o usuário autenticado.
    """
    logger.info(f"Criando assinatura para usuário {user_id}")

    # Verificar se o usuário existe
    user = await get_user_by_id(user_id)
    if not user:
        logger.warning(f"Usuário {user_id} não encontrado ao criar assinatura")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    # Criar assinatura
    return subscription_service.create_subscription(user_id=user_id, subscription_data=subscription)


@router.get(
    "/current",
    response_model=SubscriptionResponse,
    summary="Obter assinatura atual",
    description="""
    Obtém a assinatura atual do usuário autenticado.
    
    Retorna detalhes da assinatura ativa, incluindo tipo de plano, 
    status, datas de pagamento e vencimento, e gateway de pagamento utilizado.
    
    Se o usuário não possuir assinatura ativa, retorna 404.
    """,
    responses={
        200: {
            "description": "Assinatura encontrada",
            "content": {
                "application/json": {
                    "example": {
                        "id": "f8a5df6e-d182-4f3c-b8e7-1c02cd9f99a4",
                        "user_id": "5eb7cf5a-0742-42b8-a40c-fb85f3b337aa",
                        "plan_type": "PREMIUM",
                        "status": "ACTIVE",
                        "payment_gateway": "STRIPE",
                        "last_payment_date": "2023-03-29T12:34:56.123Z",
                        "next_payment_date": "2023-04-29T12:34:56.123Z",
                        "expires_at": "2023-04-29T12:34:56.123Z",
                        "created_at": "2023-03-29T12:34:56.123Z"
                    }
                }
            }
        },
        404: {
            "description": "Usuário ou assinatura não encontrados",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Assinatura não encontrada"
                    }
                }
            }
        }
    }
)
async def get_current_subscription(
    user_id: str = Depends(get_current_user_id),
    subscription_service: SubscriptionService = Depends(
        get_subscription_service)
):
    """
    Obtém a assinatura atual do usuário autenticado.
    """
    logger.info(f"Obtendo assinatura atual para usuário {user_id}")

    # Verificar se o usuário existe
    user = await get_user_by_id(user_id)
    if not user:
        logger.warning(
            f"Usuário {user_id} não encontrado ao buscar assinatura")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    # Buscar assinatura atual
    subscription = subscription_service.get_current_subscription(user_id)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assinatura não encontrada"
        )

    return subscription


@router.get(
    "/history",
    response_model=List[SubscriptionResponse],
    summary="Obter histórico de assinaturas",
    description="""
    Obtém o histórico completo de assinaturas do usuário autenticado.
    
    Retorna todas as assinaturas do usuário, inclusive as canceladas,
    expiradas ou substituídas, ordenadas da mais recente para a mais antiga.
    """,
    responses={
        200: {
            "description": "Histórico de assinaturas",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "f8a5df6e-d182-4f3c-b8e7-1c02cd9f99a4",
                            "user_id": "5eb7cf5a-0742-42b8-a40c-fb85f3b337aa",
                            "plan_type": "PREMIUM",
                            "status": "ACTIVE",
                            "payment_gateway": "STRIPE",
                            "last_payment_date": "2023-03-29T12:34:56.123Z",
                            "next_payment_date": "2023-04-29T12:34:56.123Z",
                            "expires_at": "2023-04-29T12:34:56.123Z",
                            "created_at": "2023-03-29T12:34:56.123Z"
                        },
                        {
                            "id": "a1b2c3d4-e5f6-4a5b-8c7d-9e0f1a2b3c4d",
                            "user_id": "5eb7cf5a-0742-42b8-a40c-fb85f3b337aa",
                            "plan_type": "PREMIUM",
                            "status": "CANCELLED",
                            "payment_gateway": "HOTMART",
                            "last_payment_date": "2023-01-15T10:30:00.000Z",
                            "next_payment_date": None,
                            "expires_at": "2023-02-15T10:30:00.000Z",
                            "created_at": "2023-01-15T10:30:00.000Z"
                        }
                    ]
                }
            }
        },
        404: {
            "description": "Usuário não encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Usuário não encontrado"
                    }
                }
            }
        }
    }
)
async def get_subscription_history(
    user_id: str = Depends(get_current_user_id),
    subscription_service: SubscriptionService = Depends(
        get_subscription_service)
):
    """
    Obtém o histórico de assinaturas do usuário autenticado.
    """
    logger.info(f"Obtendo histórico de assinaturas para usuário {user_id}")

    # Verificar se o usuário existe
    user = await get_user_by_id(user_id)
    if not user:
        logger.warning(
            f"Usuário {user_id} não encontrado ao buscar histórico de assinaturas")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    # Buscar histórico de assinaturas
    return subscription_service.get_user_subscriptions(user_id)


@router.put(
    "/cancel",
    response_model=SubscriptionResponse,
    summary="Cancelar assinatura atual",
    description="""
    Cancela a assinatura atual do usuário autenticado.
    
    A assinatura não é removida, mas seu status é alterado para CANCELLED.
    O usuário mantém o acesso Premium até a data de expiração (expires_at),
    mas a assinatura não será renovada automaticamente.
    """,
    responses={
        200: {
            "description": "Assinatura cancelada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": "f8a5df6e-d182-4f3c-b8e7-1c02cd9f99a4",
                        "user_id": "5eb7cf5a-0742-42b8-a40c-fb85f3b337aa",
                        "plan_type": "PREMIUM",
                        "status": "CANCELLED",
                        "payment_gateway": "STRIPE",
                        "last_payment_date": "2023-03-29T12:34:56.123Z",
                        "next_payment_date": None,
                        "expires_at": "2023-04-29T12:34:56.123Z",
                        "created_at": "2023-03-29T12:34:56.123Z"
                    }
                }
            }
        },
        404: {
            "description": "Usuário ou assinatura não encontrados",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Assinatura não encontrada"
                    }
                }
            }
        }
    }
)
async def cancel_subscription(
    user_id: str = Depends(get_current_user_id),
    subscription_service: SubscriptionService = Depends(
        get_subscription_service)
):
    """
    Cancela a assinatura atual do usuário autenticado.
    """
    logger.info(f"Cancelando assinatura para usuário {user_id}")

    # Verificar se o usuário existe
    user = await get_user_by_id(user_id)
    if not user:
        logger.warning(
            f"Usuário {user_id} não encontrado ao cancelar assinatura")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    # Cancelar assinatura
    subscription = subscription_service.cancel_subscription(user_id)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assinatura não encontrada"
        )

    return subscription
