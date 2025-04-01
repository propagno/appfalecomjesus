from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_payment_service, get_current_user_id, get_user_by_id
from app.services.payment_service import PaymentService
from app.schemas.payment import CheckoutRequest, CheckoutResponse, SubscriptionPlanResponse
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/checkout",
    response_model=CheckoutResponse,
    summary="Criar sessão de checkout",
    description="""
    Cria uma nova sessão de checkout para assinatura Premium.
    
    Este endpoint inicia o processo de pagamento para o usuário autenticado,
    gerando uma URL de checkout de acordo com o gateway selecionado (Stripe ou Hotmart).
    
    O usuário será redirecionado para a página de pagamento do gateway escolhido,
    onde poderá completar a transação. Após a conclusão ou cancelamento, o usuário
    será redirecionado para as URLs de sucesso ou cancelamento fornecidas.
    """,
    responses={
        200: {
            "description": "Sessão de checkout criada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "checkout_url": "https://checkout.stripe.com/pay/cs_test_a1b2c3d4e5f6g7h8i9j0"
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
async def create_checkout_session(
    checkout_data: CheckoutRequest,
    user_id: str = Depends(get_current_user_id),
    payment_service: PaymentService = Depends(get_payment_service)
) -> CheckoutResponse:
    """
    Cria uma nova sessão de checkout para assinatura.
    """
    logger.info(f"Criando sessão de checkout para usuário {user_id}")

    # Verificar se o usuário existe
    user = await get_user_by_id(user_id)
    if not user:
        logger.warning(f"Usuário {user_id} não encontrado ao criar checkout")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    # Criar checkout
    checkout_url = payment_service.create_checkout_session(
        user_id=user_id,
        plan_id=checkout_data.plan_id,
        success_url=checkout_data.success_url,
        cancel_url=checkout_data.cancel_url,
        payment_gateway=checkout_data.payment_gateway
    )

    return CheckoutResponse(checkout_url=checkout_url)


@router.get(
    "/plans",
    response_model=List[SubscriptionPlanResponse],
    summary="Obter planos disponíveis",
    description="""
    Retorna a lista de planos de assinatura disponíveis para compra.
    
    Este endpoint fornece informações detalhadas sobre cada plano, incluindo:
    - Identificador único do plano
    - Nome descritivo
    - Descrição detalhada dos benefícios
    - Preço e moeda
    - Intervalo de cobrança (mensal ou anual)
    
    Os planos atualmente disponíveis são Mensal e Anual, este último 
    com desconto em relação ao pagamento mensal.
    """,
    responses={
        200: {
            "description": "Lista de planos disponíveis",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "monthly",
                            "name": "Plano Mensal",
                            "description": "Acesso completo por 1 mês",
                            "price": "29.90",
                            "currency": "BRL",
                            "interval": "month",
                            "interval_count": 1
                        },
                        {
                            "id": "yearly",
                            "name": "Plano Anual",
                            "description": "Acesso completo por 1 ano com 20% de desconto",
                            "price": "287.00",
                            "currency": "BRL",
                            "interval": "year",
                            "interval_count": 1
                        }
                    ]
                }
            }
        }
    }
)
async def get_available_plans() -> List[SubscriptionPlanResponse]:
    """
    Obtém os planos de assinatura disponíveis.
    """
    logger.info("Obtendo planos de assinatura disponíveis")

    # Planos pré-definidos
    plans = [
        SubscriptionPlanResponse(
            id="monthly",
            name="Plano Mensal",
            description="Acesso completo por 1 mês",
            price="29.90",
            currency="BRL",
            interval="month",
            interval_count=1
        ),
        SubscriptionPlanResponse(
            id="yearly",
            name="Plano Anual",
            description="Acesso completo por 1 ano com 20% de desconto",
            price="287.00",
            currency="BRL",
            interval="year",
            interval_count=1
        )
    ]

    return plans


@router.get(
    "/validate-subscription",
    summary="Validar assinatura ativa",
    description="""
    Verifica se o usuário atual possui uma assinatura Premium ativa.
    
    Este endpoint é útil para o frontend verificar rapidamente o status
    da assinatura do usuário e determinar quais funcionalidades devem estar
    disponíveis, como acesso ilimitado ao chat IA ou ausência de anúncios.
    
    A resposta contém um campo booleano indicando se o usuário tem uma 
    assinatura ativa e válida.
    """,
    responses={
        200: {
            "description": "Status da assinatura do usuário",
            "content": {
                "application/json": {
                    "examples": {
                        "active": {
                            "summary": "Usuário com assinatura ativa",
                            "value": {"has_active_subscription": True}
                        },
                        "inactive": {
                            "summary": "Usuário sem assinatura ativa",
                            "value": {"has_active_subscription": False}
                        }
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
async def validate_subscription(
    user_id: str = Depends(get_current_user_id),
    payment_service: PaymentService = Depends(get_payment_service)
) -> Dict[str, bool]:
    """
    Valida se o usuário tem uma assinatura ativa.
    """
    logger.info(f"Validando assinatura para usuário {user_id}")

    # Verificar se o usuário existe
    user = await get_user_by_id(user_id)
    if not user:
        logger.warning(
            f"Usuário {user_id} não encontrado ao validar assinatura")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    # Validar assinatura
    is_active = payment_service.validate_subscription(user_id)

    return {"has_active_subscription": is_active}
