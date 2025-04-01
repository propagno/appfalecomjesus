from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime

from app.core.security import get_current_user
from app.core.cache import ChatCache
from app.schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    ChatHistoryResponse,
    RemainingMessagesResponse,
    AdRewardResponse,
    StudyPlanRequest,
    StudyPlanResponse
)
from app.services.chat_service import ChatService
from app.core.logging import get_logger
from app.core.database import db

router = APIRouter()
logger = get_logger(__name__)
chat_service = ChatService(db)
chat_cache = ChatCache()


@router.get("/health",
            status_code=status.HTTP_200_OK,
            summary="Verificação de saúde do serviço",
            description="Endpoint para verificação de saúde do serviço de chat",
            response_description="Status do serviço")
async def health_check():
    """
    Endpoint de health check para o serviço de chat.
    Não requer autenticação.
    """
    return {"status": "healthy", "service": "ms-chatia"}


@router.post("/message",
             response_model=ChatMessageResponse,
             status_code=status.HTTP_200_OK,
             summary="Envia mensagem para a IA",
             description="""
    Envia uma mensagem para a IA e recebe uma resposta personalizada.
    
    A mensagem será processada levando em conta:
    * Contexto do usuário (preferências, histórico)
    * Limites de uso (plano Free ou Premium)
    * Cache de respostas similares
    
    Se o usuário atingiu o limite diário:
    * Plano Free: Retorna erro 429 (Too Many Requests)
    * Premium: Continua normalmente
    
    A resposta inclui:
    * Mensagem da IA
    * Versículos bíblicos relevantes
    * Sugestões de próximas perguntas
    """,
             response_description="Resposta da IA com mensagem e sugestões"
             )
async def send_message(
    message: ChatMessageRequest,
    current_user=Depends(get_current_user)
):
    """
    Processa uma mensagem do usuário e retorna resposta da IA
    """
    try:
        # Verificar cache primeiro
        cached_response = await chat_cache.get_cached_response(
            user_id=current_user.id,
            message=message.message
        )
        if cached_response:
            logger.info(f"Cache hit for message from user {current_user.id}")
            return cached_response

        # Processar mensagem
        response = await chat_service.process_chat_message(
            user_id=current_user.id,
            message=message,
            is_premium=current_user.is_premium
        )

        # Salvar no cache
        await chat_cache.cache_response(
            user_id=current_user.id,
            message=message.message,
            response=response
        )

        return response

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar mensagem"
        )


@router.get("/history",
            response_model=ChatHistoryResponse,
            status_code=status.HTTP_200_OK,
            summary="Obtém histórico de chat",
            description="""
    Retorna o histórico de mensagens do usuário com paginação.
    
    Parâmetros:
    * limit: Número máximo de mensagens (default: 50)
    * skip: Número de mensagens para pular (default: 0)
    
    O histórico é ordenado por data, do mais recente ao mais antigo.
    Inclui tanto mensagens do usuário quanto respostas da IA.
    """,
            response_description="Lista paginada de mensagens do histórico"
            )
async def get_history(
    limit: int = 50,
    skip: int = 0,
    current_user=Depends(get_current_user)
):
    """
    Retorna histórico de chat do usuário
    """
    try:
        history = await chat_service.get_chat_history(
            user_id=current_user.id,
            limit=limit,
            skip=skip
        )
        return history
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar histórico"
        )


@router.get("/limit",
            response_model=RemainingMessagesResponse,
            status_code=status.HTTP_200_OK,
            summary="Verifica limite de mensagens",
            description="""
    Retorna informações sobre o limite de mensagens do usuário.
    
    Para usuários Free:
    * Limite diário de mensagens
    * Quantidade restante hoje
    * Horário de reset do limite
    
    Para usuários Premium:
    * Retorna always_unlimited=true
    """,
            response_description="Status do limite de mensagens do usuário"
            )
async def get_message_limit(
    current_user=Depends(get_current_user)
):
    """
    Retorna limite de mensagens do usuário
    """
    try:
        if current_user.is_premium:
            return {
                "always_unlimited": True,
                "remaining_messages": None,
                "reset_time": None
            }

        limit_info = await chat_service.get_message_limit(
            user_id=current_user.id
        )
        return limit_info

    except Exception as e:
        logger.error(f"Error checking limit: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao verificar limite"
        )


@router.post("/bonus",
             response_model=AdRewardResponse,
             status_code=status.HTTP_200_OK,
             summary="Adiciona mensagens bônus",
             description="""
    Adiciona mensagens bônus após usuário assistir anúncio.
    
    Disponível apenas para usuários Free.
    Adiciona +5 mensagens ao limite diário.
    Máximo de 3 bônus por dia.
    
    Retorna:
    * Novo limite de mensagens
    * Quantidade de bônus restantes hoje
    """,
             response_description="Status atualizado após adicionar bônus"
             )
async def add_bonus_messages(
    current_user=Depends(get_current_user)
):
    """
    Adiciona mensagens bônus após ver anúncio
    """
    try:
        if current_user.is_premium:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuários Premium não precisam de bônus"
            )

        bonus_info = await chat_service.add_bonus_messages(
            user_id=current_user.id
        )
        return bonus_info

    except Exception as e:
        logger.error(f"Error adding bonus: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao adicionar bônus"
        )


@router.post("/study/plan",
             response_model=StudyPlanResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Gera plano de estudo",
             description="""
    Gera um plano de estudo personalizado com base nas preferências.
    
    O plano é gerado considerando:
    * Objetivos espirituais do usuário
    * Nível de conhecimento bíblico
    * Formato preferido de conteúdo
    * Horário disponível para estudo
    
    O plano inclui:
    * Título e descrição
    * Lista de sessões diárias
    * Versículos recomendados
    * Reflexões guiadas
    """,
             response_description="Plano de estudo personalizado"
             )
async def generate_study_plan(
    preferences: StudyPlanRequest,
    current_user=Depends(get_current_user)
):
    """
    Gera plano de estudo personalizado
    """
    try:
        plan = await chat_service.generate_study_plan(
            user_id=current_user.id,
            preferences=preferences
        )
        return plan

    except Exception as e:
        logger.error(f"Error generating plan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao gerar plano de estudo"
        )
