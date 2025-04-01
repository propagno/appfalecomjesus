from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List
import logging

from app.schemas import (
    AdWatchedRequest,
    AdWatchedResponse
)
from app.dependencies import (
    get_current_user,
    get_ad_reward_service
)
from app.services import AdRewardService

# Configurar logger
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/ad-reward", response_model=AdWatchedResponse)
async def process_ad_reward(
    request_data: AdWatchedRequest,
    request: Request,
    user_id: str = Depends(get_current_user),
    ad_reward_service: AdRewardService = Depends(get_ad_reward_service)
):
    """
    Registra que um usuário assistiu a um anúncio e concede recompensa.
    Usado quando o usuário assiste a um anúncio para ganhar mais mensagens ou recursos.
    """
    try:
        # Obter IP do cliente para anti-fraude
        client_ip = request.client.host if request.client else None

        # Atualizar IP no request
        if client_ip:
            request_data.ip_address = client_ip

        # Processar recompensa
        response, success = await ad_reward_service.process_ad_watched(user_id, request_data)

        if not success:
            # Não é um erro 500, é um caso de negócio (usuário atingiu limite)
            # Retornamos 200 com sucesso=False para que o frontend possa exibir a mensagem
            return response

        return response

    except Exception as e:
        logger.error(f"Erro ao processar recompensa por anúncio: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar recompensa por anúncio"
        )


@router.get("/remaining-rewards", response_model=int)
async def get_remaining_rewards(
    user_id: str = Depends(get_current_user),
    ad_reward_service: AdRewardService = Depends(get_ad_reward_service)
):
    """
    Retorna quantas recompensas o usuário ainda pode obter hoje.
    Usado pelo frontend para verificar se deve exibir a opção de assistir anúncios.
    """
    try:
        remaining = await ad_reward_service.get_user_remaining_rewards(user_id)
        return remaining
    except Exception as e:
        logger.error(f"Erro ao verificar recompensas restantes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao verificar recompensas restantes"
        )
