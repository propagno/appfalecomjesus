from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.core.database import get_db
from app.schemas.checkout import CheckoutResponse, PaymentResponse
from app.services.checkout import CheckoutService
from app.services.subscription_service import SubscriptionService
from typing import Dict

router = APIRouter()


@router.post(
    "/checkout",
    response_model=CheckoutResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Inicia o processo de checkout",
    description="""
    Inicia o processo de checkout para assinatura de um plano.
    Gera uma sessão de pagamento no gateway escolhido (Stripe/Hotmart).
    """,
    responses={
        201: {
            "description": "Checkout iniciado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "checkout_url": "https://checkout.stripe.com/...",
                        "session_id": "cs_test_...",
                        "expires_at": "2024-03-23T11:00:00Z"
                    }
                }
            }
        },
        400: {
            "description": "Dados inválidos ou plano não encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid plan or payment gateway"
                    }
                }
            }
        },
        401: {"description": "Não autorizado"},
        403: {"description": "Usuário já possui assinatura ativa"}
    }
)
async def create_checkout(
    plan_id: str,
    payment_gateway: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Inicia o processo de checkout para assinatura de um plano.
    """
    try:
        # Verificar se usuário já tem assinatura ativa
        subscription = await SubscriptionService.get_subscription_status(db, current_user.id)
        if subscription["subscription_status"] == "active" and subscription["plan_type"] != "free":
            raise HTTPException(
                status_code=403,
                detail="User already has an active subscription"
            )

        return await CheckoutService.create_checkout_session(
            db=db,
            user_id=current_user.id,
            plan_id=plan_id,
            payment_gateway=payment_gateway
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/checkout/{session_id}",
    response_model=PaymentResponse,
    status_code=status.HTTP_200_OK,
    summary="Verifica o status do pagamento",
    description="""
    Verifica o status atual do pagamento de uma sessão de checkout.
    Retorna informações sobre o sucesso ou falha do pagamento.
    """,
    responses={
        200: {
            "description": "Status do pagamento obtido com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "status": "succeeded",
                        "payment_id": "pi_...",
                        "amount": 2990,
                        "currency": "BRL",
                        "created_at": "2024-03-23T10:00:00Z"
                    }
                }
            }
        },
        404: {
            "description": "Sessão de checkout não encontrada",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Checkout session not found"
                    }
                }
            }
        },
        401: {"description": "Não autorizado"}
    }
)
async def get_payment_status(
    session_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Verifica o status do pagamento de uma sessão de checkout.
    """
    try:
        return await CheckoutService.get_payment_status(
            db=db,
            user_id=current_user.id,
            session_id=session_id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/cancel-subscription",
    status_code=status.HTTP_200_OK,
    summary="Cancela a assinatura atual",
    description="""
    Cancela a assinatura ativa do usuário.
    O acesso ao plano premium continua até o final do período pago.
    """,
    responses={
        200: {
            "description": "Assinatura cancelada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Subscription cancelled successfully",
                        "expires_at": "2024-04-23T10:00:00Z"
                    }
                }
            }
        },
        400: {
            "description": "Usuário não possui assinatura ativa",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "No active subscription found"
                    }
                }
            }
        },
        401: {"description": "Não autorizado"}
    }
)
async def cancel_subscription(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Cancela a assinatura ativa do usuário.
    """
    try:
        return await SubscriptionService.cancel_subscription(db, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
