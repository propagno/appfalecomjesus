import stripe
from app.core.config import settings

# Configuração do Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Configuração dos preços
STRIPE_PRICES = {
    "monthly": settings.STRIPE_PRICE_ID_MONTHLY,
    "yearly": settings.STRIPE_PRICE_ID_YEARLY,
}

# Configuração das URLs de retorno
STRIPE_URLS = {
    "success": f"{settings.FRONTEND_URL}/payment/success",
    "cancel": f"{settings.FRONTEND_URL}/payment/cancel",
}


def get_stripe_price_id(plan_type: str, interval: str) -> str:
    """
    Retorna o ID do preço do Stripe baseado no tipo de plano e intervalo.

    Args:
        plan_type: Tipo do plano (monthly, yearly)
        interval: Intervalo de pagamento (month, year)

    Returns:
        str: ID do preço do Stripe
    """
    if plan_type not in STRIPE_PRICES:
        raise ValueError(f"Tipo de plano inválido: {plan_type}")
    return STRIPE_PRICES[plan_type]


def get_stripe_return_url(success: bool = True) -> str:
    """
    Retorna a URL de retorno do Stripe baseado no status do pagamento.

    Args:
        success: Se o pagamento foi bem sucedido

    Returns:
        str: URL de retorno
    """
    return STRIPE_URLS["success"] if success else STRIPE_URLS["cancel"]
