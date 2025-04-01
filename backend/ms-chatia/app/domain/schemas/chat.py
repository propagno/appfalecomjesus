from pydantic import BaseModel, Field, UUID4
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid


class ChatMessageRequest(BaseModel):
    """
    Schema para requisição de mensagem de chat.
    """
    message: str = Field(..., description="Texto da mensagem do usuário")
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Contexto adicional para a mensagem (ex: seção de estudo, plano, etc)"
    )


class ChatMessageResponse(BaseModel):
    """
    Schema para resposta de mensagem de chat.
    """
    response: str = Field(..., description="Resposta gerada pela IA")
    remaining_messages: int = Field(...,
                                    description="Número de mensagens restantes para o dia")


class ChatHistoryItem(BaseModel):
    """
    Schema para um item do histórico de chat.
    """
    id: UUID4
    message: str
    response: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """
    Schema para resposta de histórico de chat.
    """
    items: List[ChatHistoryItem]


class RemainingMessagesResponse(BaseModel):
    """
    Schema para resposta de mensagens restantes.
    """
    remaining_messages: int = Field(...,
                                    description="Número de mensagens restantes para o dia")


class AdRewardResponse(BaseModel):
    """
    Schema para resposta após assistir um anúncio.
    """
    remaining_messages: int = Field(...,
                                    description="Novo número de mensagens disponíveis")
    message: str = Field(
        default="Você ganhou mensagens adicionais!",
        description="Mensagem de sucesso"
    )


class ChatMessageCreate(BaseModel):
    """
    Schema para criação de mensagem
    """
    message: str


class ChatMessageBase(BaseModel):
    """
    Schema base para mensagem
    """
    id: str
    message: str
    response: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatHistory(BaseModel):
    """
    Schema para histórico completo
    """
    items: List[ChatHistoryItem]
    count: int


class ChatMessageLimit(BaseModel):
    """
    Schema para informações de limite
    """
    remaining_messages: int
    limit: int
    reset_in: int  # Tempo em segundos para reset


class StudyPlanRequest(BaseModel):
    """
    Requisição para geração de plano de estudo personalizado
    """
    user_id: str = Field(..., description="ID do usuário")
    name: Optional[str] = Field(None, description="Nome do usuário")
    email: Optional[str] = Field(None, description="Email do usuário")
    objectives: List[str] = Field(...,
                                  description="Objetivos espirituais do usuário")
    bible_experience_level: str = Field(
        ..., description="Nível de experiência bíblica do usuário")
    content_preferences: List[str] = Field(
        ..., description="Preferências de formato de conteúdo")
    preferred_time: str = Field(...,
                                description="Horário preferido para estudo")


class StudyPlanResponse(BaseModel):
    """
    Resposta com plano de estudo personalizado
    """
    plan: Dict[str, Any] = Field(...,
                                 description="Plano de estudo estruturado em formato JSON")
    raw_response: str = Field(..., description="Resposta bruta da IA")
