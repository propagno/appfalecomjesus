from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import uuid
import json
import logging
import httpx

from app.domain.schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    ChatHistoryResponse,
    ChatHistoryItem,
    RemainingMessagesResponse,
    AdRewardResponse,
    StudyPlanRequest,
    StudyPlanResponse
)
from app.domain.models.chat import ChatHistory
from app.infrastructure.database import get_db
from app.infrastructure.security import get_current_user_id, verify_service_api_key
from app.infrastructure.redis import get_chat_limit, decrement_chat_limit, increment_chat_limit
from app.infrastructure.openai import get_openai_service, OpenAIService
from app.core.config import get_settings, Settings

# Criar router para os endpoints de chat
chat_router = APIRouter()


@chat_router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    chat_request: ChatMessageRequest,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
    openai_service: OpenAIService = Depends(get_openai_service),
    settings: Settings = Depends(get_settings)
):
    """
    Envia uma mensagem para o chat e recebe uma resposta da IA.

    Requer autenticação JWT.

    Retorna:
        ChatMessageResponse: Resposta gerada e mensagens restantes
    """
    try:
        # Verificar limite de mensagens do usuário
        remaining = await get_chat_limit(str(user_id))

        # Se não houver mensagens restantes, retorna erro 429 (Too Many Requests)
        if remaining <= 0:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Limite diário de mensagens atingido. Assista a um anúncio para liberar mais mensagens."
            )

        # Recuperar histórico recente do usuário para contexto
        recent_history = db.query(ChatHistory).filter(
            ChatHistory.user_id == user_id
        ).order_by(ChatHistory.created_at.desc()).limit(5).all()

        # Preparar contexto para a OpenAI com mensagens anteriores
        context = []
        for item in reversed(recent_history):  # Invertemos para ordem cronológica
            context.append({"role": "user", "content": item.message})
            context.append({"role": "assistant", "content": item.response})

        # Construir o prompt principal com instruções para a IA
        prompt = f"""
        Você é um conselheiro espiritual cristão e deve responder com sabedoria baseada na Bíblia.
        
        Por favor, considere estas diretrizes:
        1. Cite ao menos um versículo relevante em cada resposta
        2. Mantenha suas respostas breves e objetivas (máximo 150 palavras)
        3. Seja acolhedor e empático
        4. Evite julgamentos e seja inclusivo
        5. Baseie suas respostas em princípios bíblicos
        
        Pergunta do usuário: {chat_request.message}
        """

        # Se houver contexto específico (ex: sessão de estudo atual), inclui no prompt
        if chat_request.context:
            context_str = str(chat_request.context)
            prompt += f"\n\nContexto adicional: {context_str}"

        # Gerar resposta da IA com OpenAI
        ai_response = await openai_service.generate_response(
            prompt=prompt,
            context=context if context else None,
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS
        )

        # Decrementar o contador de mensagens
        new_remaining = await decrement_chat_limit(str(user_id))

        # Salvar interação no banco de dados
        context_str = None
        if chat_request.context:
            context_str = str(chat_request.context)

        chat_history = ChatHistory(
            user_id=user_id,
            message=chat_request.message,
            response=ai_response,
            model_used=settings.OPENAI_MODEL,
            context=context_str
        )

        db.add(chat_history)
        db.commit()

        # Retornar resposta com limite atualizado
        return ChatMessageResponse(
            response=ai_response,
            remaining_messages=new_remaining if new_remaining >= 0 else 0
        )
    except Exception as e:
        # Log do erro para diagnóstico
        logger = logging.getLogger("chat_router")
        logger.error(f"Erro no processamento de mensagem: {str(e)}")

        # Se for um erro da OpenAI, trata adequadamente
        if "openai" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Serviço de IA temporariamente indisponível. Tente novamente em alguns instantes."
            )

        # Outros erros são propagados normalmente
        raise


@chat_router.get("/history", response_model=ChatHistoryResponse)
async def get_history(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Retorna o histórico de mensagens do usuário.

    Requer autenticação JWT.

    Retorna:
        ChatHistoryResponse: Lista de mensagens e respostas
    """
    # Buscar histórico do usuário, ordenado do mais recente para o mais antigo
    history = db.query(ChatHistory).filter(
        ChatHistory.user_id == user_id
    ).order_by(ChatHistory.created_at.desc()).all()

    # Converter para o formato de resposta
    items = [
        ChatHistoryItem(
            id=item.id,
            message=item.message,
            response=item.response,
            created_at=item.created_at
        ) for item in history
    ]

    return ChatHistoryResponse(items=items)


@chat_router.get("/remaining", response_model=RemainingMessagesResponse)
async def get_remaining_messages(
    user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Retorna o número de mensagens restantes para o dia.

    Requer autenticação JWT.

    Retorna:
        RemainingMessagesResponse: Número de mensagens restantes
    """
    remaining = await get_chat_limit(str(user_id))
    return RemainingMessagesResponse(remaining_messages=remaining)


@chat_router.post("/ad-reward", response_model=AdRewardResponse)
async def process_ad_reward(
    user_id: uuid.UUID = Depends(get_current_user_id),
    settings: Settings = Depends(get_settings)
):
    """
    Processa a recompensa após o usuário assistir a um anúncio,
    incrementando o limite diário de mensagens.

    Requer autenticação JWT.

    Retorna:
        AdRewardResponse: Novo número de mensagens disponíveis
    """
    try:
        logger = logging.getLogger("chat_router")
        logger.info(f"Processando recompensa de anúncio para usuário {user_id}")
        
        # Adiciona 5 mensagens ao limite do usuário
        bonus_messages = 5  # Número fixo de mensagens bônus
        new_remaining = await increment_chat_limit(str(user_id), bonus_messages)
        
        # Log a ação para auditoria
        logger.info(f"Usuário {user_id} recebeu +{bonus_messages} mensagens. Novo limite: {new_remaining}")
        
        # Notificar o ms-monetization sobre a recompensa processada (assíncrono)
        try:
            if settings.MS_MONETIZATION_URL:
                async with httpx.AsyncClient(timeout=2.0) as client:
                    await client.post(
                        f"{settings.MS_MONETIZATION_URL}/api/v1/monetization/log-reward",
                        json={
                            "user_id": str(user_id),
                            "reward_type": "chat_messages",
                            "reward_amount": bonus_messages,
                            "source": "ad_view"
                        },
                        headers={"Authorization": f"Bearer {settings.SERVICE_API_KEY}"}
                    )
        except Exception as notification_error:
            # Não bloqueia a operação principal se a notificação falhar
            logger.warning(f"Erro ao notificar recompensa: {str(notification_error)}")

        return AdRewardResponse(
            remaining_messages=new_remaining,
            message=f"Você ganhou +{bonus_messages} mensagens para usar hoje!"
        )
    except Exception as e:
        logger.error(f"Erro ao processar recompensa: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar recompensa de anúncio."
        )


@chat_router.post("/generate-study-plan", response_model=StudyPlanResponse)
async def generate_study_plan(
    plan_request: StudyPlanRequest,
    _: None = Depends(verify_service_api_key),
    openai_service: OpenAIService = Depends(get_openai_service),
    settings: Settings = Depends(get_settings)
):
    """
    Gera um plano de estudo personalizado com base nas preferências do usuário.
    Este endpoint é protegido por API Key e só deve ser chamado por outros microsserviços.

    Args:
        plan_request: Preferências do usuário para geração do plano

    Returns:
        StudyPlanResponse: Plano de estudo personalizado em formato estruturado
    """
    # Construir o prompt para o OpenAI com base nas preferências
    objectives = ", ".join(plan_request.objectives)
    content_formats = ", ".join(plan_request.content_preferences)

    prompt = f"""
    Crie um plano de estudo bíblico personalizado para um usuário com os seguintes objetivos e preferências:
    
    Objetivos espirituais: {objectives}
    Nível de experiência bíblica: {plan_request.bible_experience_level}
    Formatos de conteúdo preferidos: {content_formats}
    Horário preferido para estudo: {plan_request.preferred_time}
    
    O plano deve ter duração de 7 dias, com uma seção por dia. Forneça o plano no seguinte formato JSON:
    
    {{
        "title": "Título do plano",
        "description": "Descrição geral do plano",
        "sections": [
            {{
                "title": "Título da seção do dia 1",
                "description": "Descrição breve da seção",
                "day_number": 1,
                "duration_minutes": 20,
                "contents": [
                    {{
                        "content_type": "verse",
                        "content": "Texto do versículo",
                        "reference": "Referência bíblica (ex: João 3:16)"
                    }},
                    {{
                        "content_type": "reflection",
                        "content": "Texto da reflexão sobre o versículo (200-300 palavras)"
                    }},
                    {{
                        "content_type": "prayer",
                        "content": "Texto de uma oração sugerida (50-100 palavras)"
                    }},
                    {{
                        "content_type": "action",
                        "content": "Sugestão de ação prática para aplicar o aprendizado"
                    }}
                ]
            }}
            // Repetir para os dias 2 a 7
        ]
    }}
    
    Responda APENAS com o JSON, sem texto adicional antes ou depois.
    """

    try:
        # Gerar resposta com temperatura mais alta para criatividade
        ai_response = await openai_service.generate_response(
            prompt,
            model=settings.openai_model,
            temperature=0.8,
            max_tokens=4000,
            response_format={"type": "json_object"}
        )

        # Tentar fazer parse do JSON
        try:
            plan_data = json.loads(ai_response)
            return StudyPlanResponse(
                plan=plan_data,
                raw_response=ai_response
            )
        except json.JSONDecodeError as e:
            # Tentar extrair JSON manualmente se a resposta tiver texto extra
            start_idx = ai_response.find('{')
            end_idx = ai_response.rfind('}') + 1

            if start_idx == -1 or end_idx == 0:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Falha ao processar a resposta da IA: formato inválido"
                )

            json_str = ai_response[start_idx:end_idx]
            plan_data = json.loads(json_str)

            return StudyPlanResponse(
                plan=plan_data,
                raw_response=ai_response
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar plano de estudo: {str(e)}"
        )


@chat_router.post("/completion", response_model=Dict[str, str])
async def generate_completion(
    request: Dict[str, Any],
    _: None = Depends(verify_service_api_key),
    openai_service: OpenAIService = Depends(get_openai_service)
):
    """
    Endpoint genérico para obter respostas da IA com qualquer prompt.
    Usado internamente pelos microsserviços.

    Args:
        request: Contém o prompt e parâmetros opcionais como max_tokens e temperature

    Returns:
        Dict: Contém a resposta gerada
    """
    try:
        prompt = request.get("prompt")
        max_tokens = request.get("max_tokens", 1000)
        temperature = request.get("temperature", 0.7)

        if not prompt:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O campo 'prompt' é obrigatório"
            )

        # Gerar resposta da IA
        response = await openai_service.generate_response(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )

        return {"response": response}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar resposta: {str(e)}"
        )


@chat_router.get("/health")
async def health_check():
    """
    Endpoint de verificação de saúde do serviço.
    Não requer autenticação.
    """
    return {"status": "healthy", "service": "ms-chatia"}
