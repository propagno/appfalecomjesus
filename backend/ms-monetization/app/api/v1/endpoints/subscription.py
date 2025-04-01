from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict

from app.dependencies import get_current_user, get_subscription_service
from app.schemas.monetization import SubscriptionStatusResponse
from app.services.subscription_service import SubscriptionService
from app.models import SubscriptionPlan as PlanType, PaymentGateway

router = APIRouter()


@router.get(
    "/subscription-status",
    response_model=SubscriptionStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtém o status da assinatura do usuário",
    description="""
    Retorna informações detalhadas sobre a assinatura do usuário atual, incluindo:
    - Tipo do plano (free, mensal, anual)
    - Status da assinatura (active, expired)
    - Data de expiração
    - Gateway de pagamento (se aplicável)
    """,
    responses={
        200: {
            "description": "Status da assinatura obtido com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "plan_type": "free",
                        "status": "active",
                        "is_premium": False,
                        "expiration_date": None,
                        "features": {
                            "chat_messages_per_day": 5,
                            "allows_chat": True
                        },
                        "chat_messages_per_day": 5,
                        "remaining_chat_messages": 3
                    }
                }
            }
        },
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"}
    }
)
async def get_subscription_status(
    current_user=Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(
        get_subscription_service)
) -> SubscriptionStatusResponse:
    """
    Retorna o status da assinatura do usuário atual.
    """
    return await subscription_service.get_subscription_status(current_user.id)


@router.post(
    "/webhook",
    status_code=status.HTTP_200_OK,
    summary="Webhook para notificações de pagamento",
    description="""
    Endpoint para receber notificações de pagamento dos gateways (Stripe/Hotmart).
    Atualiza o status da assinatura do usuário com base no pagamento recebido.
    """,
    responses={
        200: {
            "description": "Webhook processado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Subscription updated successfully"
                    }
                }
            }
        },
        400: {
            "description": "Dados inválidos",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Missing required fields"
                    }
                }
            }
        },
        500: {"description": "Erro interno do servidor"}
    }
)
async def handle_webhook(
    payload: dict,
    subscription_service: SubscriptionService = Depends(
        get_subscription_service)
) -> Dict:
    """
    Webhook para receber notificações de pagamento dos gateways.
    """
    try:
        user_id = payload.get("user_id")
        plan_type = payload.get("plan_type")
        payment_gateway = payload.get("payment_gateway")

        if not all([user_id, plan_type, payment_gateway]):
            raise HTTPException(
                status_code=400,
                detail="Missing required fields"
            )

        # Verificar se os valores de plan_type e payment_gateway são válidos
        try:
            plan_type = PlanType(plan_type)
            payment_gateway = PaymentGateway(payment_gateway)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid value: {str(e)}"
            )

        # Criar ou atualizar a assinatura
        subscription = await subscription_service.create_subscription(
            user_id=user_id,
            plan_type=plan_type,
            payment_gateway=payment_gateway
        )

        return {
            "status": "success",
            "message": "Subscription updated successfully",
            "subscription_id": str(subscription.id)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
