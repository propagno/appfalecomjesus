from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional, List
from app.models.ad_reward import AdType, RewardType
from enum import Enum


class RewardType(str, Enum):
    """Tipos de recompensas disponíveis no sistema."""
    CHAT_MESSAGES = "chat_messages"
    STUDY_DAYS = "study_days"
    POINTS = "points"


class AdType(str, Enum):
    """Tipos de anúncios suportados pelo sistema."""
    VIDEO = "video"
    BANNER = "banner"
    INTERACTIVE = "interactive"


class AdRewardBase(BaseModel):
    """Schema base para AdReward."""
    ad_type: AdType = Field(..., description="Tipo de anúncio assistido")
    reward_type: RewardType = Field(...,
                                    description="Tipo de recompensa recebida")
    reward_value: int = Field(...,
                              description="Valor da recompensa (mensagens, dias, pontos)")


class AdRewardCreate(AdRewardBase):
    """Schema para criação de AdReward."""
    ad_type: AdType
    reward_type: RewardType = Field(default=RewardType.CHAT_MESSAGES)
    reward_value: int = Field(default=5, ge=1, le=20,
                              description="Valor entre 1 e 20")


class AdReward(AdRewardBase):
    """Schema para representação completa de AdReward."""
    id: str
    user_id: str
    watched_at: datetime

    class Config:
        orm_mode = True


class AdRewardResponse(BaseModel):
    """Schema para resposta de AdReward."""
    id: str
    user_id: str
    ad_type: str
    reward_type: str
    reward_value: int
    watched_at: datetime

    class Config:
        orm_mode = True


class AdRewardList(BaseModel):
    """Schema para listagem de AdRewards."""
    items: List[AdRewardResponse]
    total: int


class AdWatchedRequest(BaseModel):
    """
    Schema para requisição de anúncio assistido.
    """
    ad_provider: str = Field(...,
                             description="Provedor do anúncio (ex: google_ads, unity_ads)")
    ad_id: Optional[str] = Field(
        None, description="ID do anúncio assistido, se disponível")
    reward_type: str = Field(
        ..., description="Tipo de recompensa desejada: chat_messages, study_days")
    ip_address: Optional[str] = Field(
        None, description="Endereço IP do cliente, preenchido automaticamente se não fornecido")

    class Config:
        json_schema_extra = {
            "example": {
                "ad_provider": "google_ads",
                "ad_id": "ca-app-pub-123456789",
                "reward_type": "chat_messages",
                "ip_address": "192.168.1.1"
            }
        }


class AdWatchedResponse(BaseModel):
    """
    Schema para resposta após anúncio assistido.
    """
    success: bool = Field(...,
                          description="Se a recompensa foi concedida com sucesso")
    reward_type: str = Field(..., description="Tipo de recompensa concedida")
    reward_value: int = Field(..., description="Valor da recompensa concedida")
    message: str = Field(...,
                         description="Mensagem descritiva sobre a recompensa")
    updated_chat_limit: Optional[int] = Field(
        None, description="Novo limite de mensagens, se aplicável")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "reward_type": "chat_messages",
                "reward_value": 5,
                "message": "Você ganhou 5 mensagens adicionais de chat!",
                "updated_chat_limit": 10
            }
        }
