from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Dict, List

from app.dependencies import get_current_user, get_ad_reward_service
from app.schemas.ad_reward import AdWatchedRequest, AdWatchedResponse
from app.services.ad_reward_service import AdRewardService
from app.models import RewardType

router = APIRouter()


@router.post(
    "/ad-reward",
    response_model=AdWatchedResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registra uma recompensa por visualização de anúncio",
    description="""
    Registra que o usuário assistiu a um anúncio e concede recompensas extras.
    Recompensas disponíveis:
    - 5 mensagens extras no chat IA
    - 1 dia extra de acesso ao plano de estudo
    """,
    responses={
        201: {
            "description": "Recompensa registrada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "reward_type": "chat_messages",
                        "reward_value": 5,
                        "message": "Você ganhou 5 mensagens adicionais de chat!",
                        "updated_chat_limit": 10
                    }
                }
            }
        },
        400: {
            "description": "Dados inválidos ou limite diário atingido",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Daily ad reward limit reached"
                    }
                }
            }
        },
        401: {"description": "Não autorizado"},
        403: {"description": "Usuário premium não pode receber recompensas por anúncios"}
    }
)
async def register_ad_reward(
    request: AdWatchedRequest,
    client_request: Request,
    current_user=Depends(get_current_user),
    ad_reward_service: AdRewardService = Depends(get_ad_reward_service)
) -> AdWatchedResponse:
    """
    Registra uma recompensa por visualização de anúncio.
    """
    try:
        # Validar o tipo de recompensa
        try:
            reward_type = RewardType(request.reward_type)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de recompensa inválido: {request.reward_type}"
            )

        # Adicionar IP do cliente se não fornecido
        if not request.ip_address:
            request.ip_address = client_request.client.host

        # Processar a recompensa
        response, success = await ad_reward_service.process_ad_watched(
            user_id=current_user.id,
            request=request
        )

        if not success:
            return response

        # Definir status code 201 (Created)
        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/remaining-ad-rewards",
    status_code=status.HTTP_200_OK,
    summary="Retorna a quantidade de recompensas disponíveis no dia",
    description="""
    Informa quantas recompensas o usuário ainda pode receber por visualizar anúncios hoje.
    Útil para mostrar no frontend quantos anúncios o usuário ainda pode assistir.
    """,
    responses={
        200: {
            "description": "Quantidade de recompensas disponíveis",
            "content": {
                "application/json": {
                    "example": {
                        "remaining_rewards": 2,
                        "max_daily_rewards": 3
                    }
                }
            }
        },
        401: {"description": "Não autorizado"}
    }
)
async def get_remaining_ad_rewards(
    current_user=Depends(get_current_user),
    ad_reward_service: AdRewardService = Depends(get_ad_reward_service)
) -> Dict:
    """
    Retorna quantas recompensas o usuário ainda pode receber por visualizar anúncios hoje.
    """
    try:
        remaining = await ad_reward_service.get_user_remaining_rewards(current_user.id)
        return {
            "remaining_rewards": remaining,
            "max_daily_rewards": ad_reward_service.MAX_DAILY_REWARDS
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
