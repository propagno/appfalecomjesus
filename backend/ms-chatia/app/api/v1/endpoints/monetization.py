from typing import Dict, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.logging import get_logger
from app.schemas.monetization import (
    Subscription,
    SubscriptionPlan,
    AdReward,
    PaymentIntent
)
from app.services.monetization_service import MonetizationService

router = APIRouter()
logger = get_logger(__name__)


@router.get(
    "/plans",
    response_model=List[SubscriptionPlan],
    summary="Listar planos",
    description="""
    Lista todos os planos de assinatura disponíveis.
    
    Inclui:
    - Plano Free (gratuito)
    - Plano Premium Mensal
    - Plano Premium Anual
    
    Cada plano detalha:
    - Preço
    - Benefícios
    - Limites
    - Descontos ativos
    """
)
async def list_plans(
    db: Session = Depends(get_db)
) -> List[SubscriptionPlan]:
    """
    Lista planos disponíveis.

    Args:
        db: Sessão do banco de dados

    Returns:
        Lista de SubscriptionPlan

    Raises:
        HTTPException: Se erro ao listar
    """
    try:
        monetization_service = MonetizationService(db)
        return await monetization_service.list_plans()
    except Exception as e:
        logger.error(f"Error listing plans: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar planos"
        )


@router.get(
    "/subscription",
    response_model=Subscription,
    summary="Assinatura atual",
    description="""
    Retorna detalhes da assinatura atual do usuário.
    
    Inclui:
    - Plano atual
    - Status (ativo/inativo)
    - Data de expiração
    - Método de pagamento
    - Histórico de pagamentos
    """
)
async def get_subscription(
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> Subscription:
    """
    Retorna assinatura atual.

    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Subscription com detalhes

    Raises:
        HTTPException: Se erro ao buscar
    """
    try:
        monetization_service = MonetizationService(db)
        return await monetization_service.get_subscription(
            user_id=current_user["id"]
        )
    except Exception as e:
        logger.error(f"Error getting subscription: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar assinatura"
        )


@router.post(
    "/checkout",
    response_model=PaymentIntent,
    summary="Iniciar checkout",
    description="""
    Inicia processo de checkout para assinatura Premium.
    
    Integrado com:
    - Stripe (cartão)
    - Hotmart (pix, boleto)
    
    Retorna URL segura para pagamento.
    """
)
async def create_checkout(
    plan_id: UUID,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> PaymentIntent:
    """
    Inicia checkout para assinatura.

    Args:
        plan_id: ID do plano
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        PaymentIntent com URL

    Raises:
        HTTPException: Se erro no checkout
    """
    try:
        monetization_service = MonetizationService(db)
        return await monetization_service.create_checkout(
            user_id=current_user["id"],
            plan_id=plan_id
        )
    except Exception as e:
        logger.error(f"Error creating checkout: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao iniciar checkout"
        )


@router.post(
    "/webhook",
    status_code=status.HTTP_200_OK,
    summary="Webhook de pagamento",
    description="""
    Recebe webhooks do Stripe e Hotmart.
    
    Processa eventos como:
    - Pagamento confirmado
    - Assinatura cancelada
    - Cartão recusado
    - Reembolso
    """
)
async def payment_webhook(
    payload: Dict,
    db: Session = Depends(get_db)
):
    """
    Processa webhook de pagamento.

    Args:
        payload: Dados do webhook
        db: Sessão do banco de dados

    Raises:
        HTTPException: Se erro no processamento
    """
    try:
        monetization_service = MonetizationService(db)
        await monetization_service.process_webhook(payload)
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar webhook"
        )


@router.post(
    "/ad-reward",
    response_model=AdReward,
    summary="Recompensa por anúncio",
    description="""
    Registra visualização de anúncio e libera recompensa.
    
    Disponível para usuários Free:
    - +5 mensagens no chat
    - +1 dia de estudo
    - +10 pontos de gamificação
    
    Limite de 3 recompensas por dia.
    """
)
async def register_ad_reward(
    ad_type: str,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> AdReward:
    """
    Registra recompensa por anúncio.

    Args:
        ad_type: Tipo do anúncio
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        AdReward com detalhes

    Raises:
        HTTPException: Se erro ao registrar
    """
    try:
        monetization_service = MonetizationService(db)
        return await monetization_service.register_ad_reward(
            user_id=current_user["id"],
            ad_type=ad_type
        )
    except Exception as e:
        logger.error(f"Error registering ad reward: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao registrar recompensa"
        )


@router.get(
    "/ad-rewards/remaining",
    response_model=int,
    summary="Recompensas restantes",
    description="""
    Retorna quantidade de recompensas ainda disponíveis hoje.
    
    Máximo de 3 por dia para usuários Free.
    Reseta à meia-noite.
    """
)
async def get_remaining_rewards(
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> int:
    """
    Retorna recompensas restantes.

    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Número de recompensas

    Raises:
        HTTPException: Se erro ao buscar
    """
    try:
        monetization_service = MonetizationService(db)
        return await monetization_service.get_remaining_rewards(
            user_id=current_user["id"]
        )
    except Exception as e:
        logger.error(f"Error getting remaining rewards: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar recompensas"
        )
