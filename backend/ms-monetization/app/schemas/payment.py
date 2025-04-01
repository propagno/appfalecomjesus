from pydantic import BaseModel, Field
from typing import Optional


class CheckoutRequest(BaseModel):
    """Request para criação de checkout."""
    plan_id: str = Field(..., description="ID do plano de assinatura")
    success_url: str = Field(...,
                             description="URL de redirecionamento em caso de sucesso")
    cancel_url: str = Field(...,
                            description="URL de redirecionamento em caso de cancelamento")
    payment_gateway: str = Field(...,
                                 description="Gateway de pagamento (stripe, hotmart)")


class CheckoutResponse(BaseModel):
    """Response para criação de checkout."""
    checkout_url: str = Field(...,
                              description="URL de checkout para redirecionamento")


class SubscriptionPlanResponse(BaseModel):
    """Response para planos de assinatura."""
    id: str = Field(..., description="ID do plano")
    name: str = Field(..., description="Nome do plano")
    description: str = Field(..., description="Descrição do plano")
    price: str = Field(..., description="Preço do plano")
    currency: str = Field(..., description="Moeda do plano")
    interval: str = Field(...,
                          description="Intervalo de cobrança (month, year)")
    interval_count: int = Field(..., description="Quantidade de intervalos")
    features: Optional[list[str]] = Field(
        None, description="Lista de recursos incluídos no plano")
