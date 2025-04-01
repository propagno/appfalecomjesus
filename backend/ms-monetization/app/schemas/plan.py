from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional


class PlanBase(BaseModel):
    """Schema base para planos"""
    name: str = Field(..., description="Nome do plano")
    description: str = Field(..., description="Descrição do plano")
    price_monthly: int = Field(..., description="Preço mensal em centavos")
    price_yearly: int = Field(..., description="Preço anual em centavos")
    features: Dict = Field(..., description="Recursos do plano")


class PlanCreate(PlanBase):
    """Schema para criação de plano"""
    pass


class PlanUpdate(PlanBase):
    """Schema para atualização de plano"""
    name: Optional[str] = None
    description: Optional[str] = None
    price_monthly: Optional[int] = None
    price_yearly: Optional[int] = None
    features: Optional[Dict] = None


class PlanResponse(PlanBase):
    """Schema para resposta de plano"""
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "11111111-1111-1111-1111-111111111111",
                "name": "Free",
                "description": "Acesso básico ao sistema",
                "price_monthly": 0,
                "price_yearly": 0,
                "features": {
                    "chat_messages_per_day": 5,
                    "study_days_per_month": 10,
                    "has_ads": True
                },
                "created_at": "2024-03-23T10:00:00Z"
            }
        }


class PlanListResponse(BaseModel):
    """Schema para lista de planos"""
    plans: List[PlanResponse]

    class Config:
        json_schema_extra = {
            "example": {
                "plans": [
                    {
                        "id": "11111111-1111-1111-1111-111111111111",
                        "name": "Free",
                        "description": "Acesso básico ao sistema",
                        "price_monthly": 0,
                        "price_yearly": 0,
                        "features": {
                            "chat_messages_per_day": 5,
                            "study_days_per_month": 10,
                            "has_ads": True
                        },
                        "created_at": "2024-03-23T10:00:00Z"
                    },
                    {
                        "id": "22222222-2222-2222-2222-222222222222",
                        "name": "Premium",
                        "description": "Acesso ilimitado a todos os recursos",
                        "price_monthly": 2990,
                        "price_yearly": 29900,
                        "features": {
                            "chat_messages_per_day": -1,
                            "study_days_per_month": -1,
                            "has_ads": False
                        },
                        "created_at": "2024-03-23T10:00:00Z"
                    }
                ]
            }
        }
