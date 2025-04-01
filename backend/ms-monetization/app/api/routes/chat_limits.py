from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from app.api.deps import (
    get_db,
    get_current_user_id,
    get_subscription_service,
    get_ad_reward_service,
    get_chat_limit_service
)
from app.services.chat_limit_service import ChatLimitService
from app.services.ad_reward_service import AdRewardService
from app.services.subscription_service import SubscriptionService
from app.schemas.ad_reward import AdRewardCreate
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/check",
    response_model=Dict[str, Any],
    summary="Verificar limite de mensagens disponíveis",
    description="""
    Verifica o limite atual de mensagens de chat disponíveis para o usuário.
    
    Usuários Premium têm acesso ilimitado ao chat (retornará -1).
    Usuários Free têm um limite diário (por padrão 5 mensagens) que é renovado cada dia.
    """
)
async def check_chat_limit(
    user_id: str = Depends(get_current_user_id),
    chat_limit_service: ChatLimitService = Depends(get_chat_limit_service),
    subscription_service: SubscriptionService = Depends(
        get_subscription_service)
):
    """
    Verifica o limite de mensagens de chat do usuário atual.

    Retorna informações sobre o status do limite (se possui limite, quantidade disponível, se é premium)
    e uma mensagem explicativa para o usuário.

    Usuários premium têm acesso ilimitado (-1).
    Usuários Free têm um limite diário que é verificado e decrementado a cada uso.
    """
    try:
        result = await chat_limit_service.check_limit(user_id, subscription_service)
        return result
    except Exception as e:
        logger.error(f"Erro ao verificar limite de chat: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao verificar limite de chat: {str(e)}"
        )


@router.post(
    "/use",
    response_model=Dict[str, Any],
    summary="Registrar uso de uma mensagem",
    description="""
    Registra o uso de uma mensagem do chat, decrementando o limite diário do usuário.
    
    Para usuários Premium, o uso é sempre permitido e não afeta nenhum contador.
    Para usuários Free, o limite é decrementado a cada uso. Quando o limite 
    chegar a zero, o usuário precisará assistir a um anúncio ou fazer upgrade.
    """,
    responses={
        200: {
            "description": "Mensagem enviada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "is_premium": False,
                        "available_messages": 4,
                        "message": "Mensagem enviada com sucesso."
                    }
                }
            }
        },
        403: {
            "description": "Limite excedido",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Limite de mensagens excedido. Assista a um anúncio para ganhar mais mensagens ou faça upgrade para Premium."
                    }
                }
            }
        }
    }
)
async def use_chat_message(
    user_id: str = Depends(get_current_user_id),
    chat_limit_service: ChatLimitService = Depends(get_chat_limit_service),
    subscription_service: SubscriptionService = Depends(
        get_subscription_service)
):
    """
    Decrementa o limite de mensagens de chat do usuário após envio de uma mensagem.

    Verifica se o usuário é premium ou tem limite disponível, e decrementa o contador
    caso seja um usuário Free. Retorna o status atualizado do limite.

    Se o usuário não tiver limite disponível, retorna erro 403 Forbidden.
    """
    try:
        # Primeiro verificar se o usuário tem limite disponível
        check_result = await chat_limit_service.check_limit(user_id, subscription_service)

        if not check_result["has_limit"]:
            logger.warning(
                f"Usuário {user_id} tentou enviar mensagem sem limite disponível")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Limite de mensagens excedido. Assista a um anúncio para ganhar mais mensagens ou faça upgrade para Premium."
            )

        # Decrementar o limite
        result = await chat_limit_service.decrement_limit(user_id, subscription_service)
        logger.info(
            f"Mensagem enviada por usuário {user_id}, novo limite: {result.get('available_messages', -1)}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao registrar uso de mensagem: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao registrar uso de mensagem: {str(e)}"
        )


@router.post(
    "/reward-from-ad",
    response_model=Dict[str, Any],
    summary="Adicionar mensagens por visualização de anúncio",
    description="""
    Incrementa o limite de mensagens de chat após o usuário assistir a um anúncio.
    
    Registra a visualização do anúncio no histórico e adiciona mensagens extras 
    ao limite diário do usuário. Por padrão, cada visualização concede 5 mensagens adicionais.
    
    Existe um limite diário de recompensas por anúncios que o usuário pode receber.
    """,
    responses={
        200: {
            "description": "Recompensa concedida com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "available_messages": 10,
                        "message": "Você ganhou 5 mensagens adicionais de chat!"
                    }
                }
            }
        },
        500: {
            "description": "Erro ao processar recompensa",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Erro ao registrar recompensa. Tente novamente."
                    }
                }
            }
        }
    }
)
async def reward_from_ad(
    reward_data: AdRewardCreate,
    user_id: str = Depends(get_current_user_id),
    chat_limit_service: ChatLimitService = Depends(get_chat_limit_service),
    ad_reward_service: AdRewardService = Depends(get_ad_reward_service),
    db: Session = Depends(get_db)
):
    """
    Incrementa o limite de mensagens de chat após o usuário assistir a um anúncio.

    Registra a recompensa no histórico de AdReward e incrementa o limite de mensagens
    no Redis para o usuário.

    A recompensa padrão é de 5 mensagens adicionais, mas pode ser configurada no request.
    """
    try:
        # Primeiro registrar a visualização do anúncio no histórico
        logger.info(
            f"Registrando recompensa por anúncio para usuário {user_id}: {reward_data.reward_value} mensagens")

        ad_reward = ad_reward_service.create_ad_reward(
            db=db,
            user_id=user_id,
            ad_type=reward_data.ad_type,
            reward_type="chat_messages",
            reward_value=reward_data.reward_value
        )

        if not ad_reward:
            logger.error(
                f"Erro ao registrar recompensa por anúncio para usuário {user_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao registrar recompensa. Tente novamente."
            )

        # Incrementar o limite de mensagens no Redis
        result = await chat_limit_service.increment_limit_from_ad(
            user_id=user_id,
            messages=reward_data.reward_value
        )

        logger.info(
            f"Limite incrementado com sucesso para usuário {user_id}: {result}")
        return result
    except Exception as e:
        logger.error(f"Erro ao processar recompensa: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar recompensa: {str(e)}"
        )
