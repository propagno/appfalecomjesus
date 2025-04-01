from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.api.deps import (
    get_db,
    get_current_user_id,
    get_ad_reward_service,
    get_user_by_id
)
from app.services.ad_reward_service import AdRewardService
from app.schemas.ad_reward import AdRewardCreate, AdRewardList, AdRewardResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/",
    response_model=AdRewardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nova recompensa por anúncio",
    description="""
    Registra uma nova recompensa obtida por visualização de anúncio.
    
    Quando um usuário Free assiste a um anúncio, ele recebe uma recompensa 
    que pode ser usada para aumentar seu limite diário de mensagens no chat,
    obter dias adicionais de estudo ou pontos no sistema de gamificação.
    
    Existe um limite máximo diário de recompensas por anúncios que um usuário pode receber.
    """,
    responses={
        201: {
            "description": "Recompensa registrada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": "f8a5df6e-d182-4f3c-b8e7-1c02cd9f99a4",
                        "user_id": "5eb7cf5a-0742-42b8-a40c-fb85f3b337aa",
                        "ad_type": "video",
                        "reward_type": "chat_messages",
                        "reward_value": 5,
                        "watched_at": "2023-03-29T12:34:56.123Z"
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
        },
        429: {
            "description": "Limite diário excedido",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Você atingiu o limite de recompensas por anúncios hoje. Tente novamente amanhã."
                    }
                }
            }
        }
    }
)
def create_ad_reward(
    reward_data: AdRewardCreate,
    user_id: str = Depends(get_current_user_id),
    ad_reward_service: AdRewardService = Depends(get_ad_reward_service),
    db: Session = Depends(get_db)
):
    """
    Registra uma nova recompensa por visualização de anúncio.

    Usado quando o usuário assiste a um anúncio e recebe uma recompensa,
    como mensagens adicionais no chat, dias extras de estudo ou pontos.
    """
    logger.info(f"Registrando recompensa por anúncio para usuário {user_id}")

    # Verificar se o usuário existe
    user = get_user_by_id(user_id)
    if not user:
        logger.warning(
            f"Usuário {user_id} não encontrado ao registrar recompensa")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    # Verificar se o usuário pode receber mais recompensas hoje
    if not ad_reward_service.can_receive_reward(db, user_id):
        logger.warning(
            f"Usuário {user_id} atingiu o limite de recompensas por anúncios hoje")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Você atingiu o limite de recompensas por anúncios hoje. Tente novamente amanhã."
        )

    # Criar a recompensa
    ad_reward = ad_reward_service.create_ad_reward(
        db=db,
        user_id=user_id,
        ad_type=reward_data.ad_type.value,
        reward_type=reward_data.reward_type.value,
        reward_value=reward_data.reward_value
    )

    if not ad_reward:
        logger.error(f"Erro ao processar recompensa para usuário {user_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar recompensa. Tente novamente."
        )

    return ad_reward


@router.get(
    "/",
    response_model=AdRewardList,
    summary="Listar recompensas do usuário",
    description="""
    Lista todas as recompensas obtidas pelo usuário por visualização de anúncios.
    
    Os resultados são paginados e podem ser filtrados por data ou tipo de recompensa.
    A lista é ordenada da mais recente para a mais antiga.
    """,
    responses={
        200: {
            "description": "Lista de recompensas obtida com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "id": "f8a5df6e-d182-4f3c-b8e7-1c02cd9f99a4",
                                "user_id": "5eb7cf5a-0742-42b8-a40c-fb85f3b337aa",
                                "ad_type": "video",
                                "reward_type": "chat_messages",
                                "reward_value": 5,
                                "watched_at": "2023-03-29T12:34:56.123Z"
                            }
                        ],
                        "total": 1
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
def list_user_rewards(
    skip: int = Query(
        0, ge=0, description="Número de registros para pular (paginação)"),
    limit: int = Query(100, ge=1, le=100,
                       description="Número máximo de registros a retornar"),
    user_id: str = Depends(get_current_user_id),
    ad_reward_service: AdRewardService = Depends(get_ad_reward_service),
    db: Session = Depends(get_db)
):
    """
    Lista o histórico de recompensas por anúncios do usuário.

    Retorna uma lista paginada de recompensas recebidas.
    """
    logger.info(f"Obtendo recompensas por anúncios para usuário {user_id}")

    # Verificar se o usuário existe
    user = get_user_by_id(user_id)
    if not user:
        logger.warning(
            f"Usuário {user_id} não encontrado ao buscar recompensas")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    # Buscar recompensas
    return ad_reward_service.get_user_rewards(db, user_id, skip, limit)


@router.get(
    "/daily-limit",
    response_model=Dict[str, Any],
    summary="Verificar limite diário de recompensas",
    description="""
    Verifica o limite diário de recompensas por visualização de anúncios.
    
    Os usuários têm um limite máximo de recompensas que podem obter por dia 
    (por padrão 3). Este endpoint retorna quantas recompensas o usuário já 
    recebeu hoje e quantas ainda pode receber.
    """,
    responses={
        200: {
            "description": "Informações sobre o limite diário",
            "content": {
                "application/json": {
                    "example": {
                        "today_count": 1,
                        "max_daily": 3,
                        "remaining": 2,
                        "can_receive": True
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
def check_daily_limit(
    user_id: str = Depends(get_current_user_id),
    ad_reward_service: AdRewardService = Depends(get_ad_reward_service),
    db: Session = Depends(get_db)
):
    """
    Verifica o limite diário de recompensas por anúncios.

    Retorna informações sobre quantas recompensas o usuário já recebeu hoje
    e quantas ainda pode receber.
    """
    logger.info(
        f"Verificando limite diário de recompensas para usuário {user_id}")

    # Verificar se o usuário existe
    user = get_user_by_id(user_id)
    if not user:
        logger.warning(
            f"Usuário {user_id} não encontrado ao verificar limite diário")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    max_daily = 3  # Máximo de recompensas diárias

    today_count = ad_reward_service.get_today_reward_count(db, user_id)
    remaining = max(0, max_daily - today_count)

    return {
        "today_count": today_count,
        "max_daily": max_daily,
        "remaining": remaining,
        "can_receive": remaining > 0
    }
