from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CheckoutResponse(BaseModel):
    """Schema para resposta do checkout"""
    checkout_url: str = Field(...,
                              description="URL do checkout no gateway de pagamento")
    session_id: str = Field(..., description="ID da sessão de checkout")
    expires_at: datetime = Field(...,
                                 description="Data e hora de expiração da sessão")

    class Config:
        json_schema_extra = {
            "example": {
                "checkout_url": "https://checkout.stripe.com/...",
                "session_id": "cs_test_...",
                "expires_at": "2024-03-23T11:00:00Z"
            }
        }


class PaymentResponse(BaseModel):
    """Schema para resposta do status do pagamento"""
    status: str = Field(...,
                        description="Status do pagamento (succeeded, failed, pending)")
    payment_id: str = Field(..., description="ID do pagamento no gateway")
    amount: int = Field(..., description="Valor do pagamento em centavos")
    currency: str = Field(..., description="Moeda do pagamento (BRL)")
    created_at: datetime = Field(..., description="Data e hora do pagamento")
    error_message: Optional[str] = Field(
        None, description="Mensagem de erro em caso de falha")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "succeeded",
                "payment_id": "pi_...",
                "amount": 2990,
                "currency": "BRL",
                "created_at": "2024-03-23T10:00:00Z"
            }
        }
