from datetime import datetime
from uuid import UUID
from typing import Optional, List, Dict

from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    """
    Requisição de mensagem para o chat
    """
    message: str = Field(
        ...,
        title="Mensagem",
        description="Texto da mensagem enviada pelo usuário",
        min_length=1,
        max_length=1000,
        example="Como posso lidar com a ansiedade segundo a Bíblia?"
    )
    context: Optional[str] = Field(
        None,
        title="Contexto",
        description="Contexto adicional para a mensagem (opcional)",
        max_length=500,
        example="Tenho sentido muita ansiedade no trabalho"
    )


class ChatMessageCreate(ChatMessageRequest):
    """Schema para criação de mensagem do chat"""
    pass


class ChatMessageResponse(BaseModel):
    """
    Resposta da IA para uma mensagem
    """
    message: str = Field(
        ...,
        title="Mensagem",
        description="Resposta gerada pela IA",
        example="A Bíblia nos ensina em Filipenses 4:6-7: 'Não andeis ansiosos por coisa alguma...'"
    )
    verses: List[str] = Field(
        ...,
        title="Versículos",
        description="Lista de versículos bíblicos relevantes",
        example=["Filipenses 4:6-7", "Mateus 6:25-34"]
    )
    suggestions: List[str] = Field(
        ...,
        title="Sugestões",
        description="Sugestões de próximas perguntas",
        example=["Como meditar na Palavra?", "O que a Bíblia diz sobre paz?"]
    )


class ChatHistoryItem(BaseModel):
    """
    Item do histórico de chat
    """
    id: UUID = Field(
        ...,
        title="ID",
        description="Identificador único da mensagem"
    )
    message: str = Field(
        ...,
        title="Mensagem",
        description="Texto enviado pelo usuário"
    )
    response: str = Field(
        ...,
        title="Resposta",
        description="Resposta gerada pela IA"
    )
    created_at: datetime = Field(
        ...,
        title="Data",
        description="Data e hora da mensagem"
    )


class ChatHistoryResponse(BaseModel):
    """
    Resposta com histórico de chat paginado
    """
    items: List[ChatHistoryItem] = Field(
        ...,
        title="Itens",
        description="Lista de mensagens do histórico"
    )
    total: int = Field(
        ...,
        title="Total",
        description="Total de mensagens no histórico"
    )
    limit: int = Field(
        ...,
        title="Limite",
        description="Limite de mensagens por página"
    )
    skip: int = Field(
        ...,
        title="Skip",
        description="Número de mensagens puladas"
    )


class RemainingMessagesResponse(BaseModel):
    """
    Resposta com informações sobre limite de mensagens
    """
    always_unlimited: bool = Field(
        ...,
        title="Ilimitado",
        description="Se o usuário tem mensagens ilimitadas (Premium)",
        example=False
    )
    remaining_messages: Optional[int] = Field(
        None,
        title="Restantes",
        description="Número de mensagens restantes hoje",
        example=5
    )
    reset_time: Optional[datetime] = Field(
        None,
        title="Reset",
        description="Horário de reset do limite diário",
        example="2025-03-24T00:00:00Z"
    )


class AdRewardResponse(BaseModel):
    """
    Resposta após assistir anúncio
    """
    messages_added: int = Field(
        ...,
        title="Adicionadas",
        description="Número de mensagens adicionadas",
        example=5
    )
    remaining_messages: int = Field(
        ...,
        title="Restantes",
        description="Total de mensagens restantes",
        example=10
    )
    remaining_rewards: int = Field(
        ...,
        title="Recompensas",
        description="Número de recompensas ainda disponíveis hoje",
        example=2
    )


class StudyPlanRequest(BaseModel):
    """
    Requisição para gerar plano de estudo
    """
    objectives: List[str] = Field(
        ...,
        title="Objetivos",
        description="Lista de objetivos espirituais",
        min_items=1,
        max_items=5,
        example=["ansiedade", "sabedoria"]
    )
    bible_experience: str = Field(
        ...,
        title="Experiência",
        description="Nível de conhecimento bíblico",
        example="iniciante"
    )
    content_preferences: List[str] = Field(
        ...,
        title="Preferências",
        description="Formatos de conteúdo preferidos",
        example=["texto", "audio"]
    )
    study_time: str = Field(
        ...,
        title="Horário",
        description="Horário preferido para estudo",
        example="manhã"
    )


class StudyPlanResponse(BaseModel):
    """
    Resposta com plano de estudo gerado
    """
    id: UUID = Field(
        ...,
        title="ID",
        description="Identificador único do plano"
    )
    title: str = Field(
        ...,
        title="Título",
        description="Título do plano de estudo",
        example="Paz Interior com João"
    )
    description: str = Field(
        ...,
        title="Descrição",
        description="Descrição detalhada do plano",
        example="Um plano de 7 dias focado em encontrar paz através do Evangelho de João"
    )
    duration_days: int = Field(
        ...,
        title="Duração",
        description="Duração do plano em dias",
        example=7
    )
    daily_duration: int = Field(
        ...,
        title="Duração Diária",
        description="Duração estimada por dia em minutos",
        example=20
    )
    sessions: List[dict] = Field(
        ...,
        title="Sessões",
        description="Lista de sessões diárias",
        example=[{
            "day": 1,
            "title": "Encontrando Paz em João 14",
            "verses": ["João 14:27"],
            "content": "Reflexão sobre a paz que Jesus oferece...",
            "duration_minutes": 20
        }]
    )


class ChatMessageLimit(BaseModel):
    """Schema para informações de limite de mensagens"""
    remaining_messages: int = Field(...,
                                    description="Mensagens restantes para hoje")
    limit: int = Field(..., description="Limite total de mensagens por dia")
    reset_in: int = Field(..., description="Segundos até o reset do limite")
    can_watch_ad: bool = Field(
        True, description="Se pode assistir anúncio para ganhar mais mensagens")
