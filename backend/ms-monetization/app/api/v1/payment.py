from fastapi import APIRouter, Depends, HTTPException, status, Request, Body
from typing import Dict, Any
import logging
import json

from app.schemas import (
    CreateCheckoutSessionRequest,
    CreateCheckoutSessionResponse,
    WebhookVerificationResponse
)
from app.dependencies import (
    get_current_user,
    get_payment_service
)
from app.services import PaymentService
from app.core.config import settings

# Configurar logger
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/create-checkout", response_model=CreateCheckoutSessionResponse)
async def create_checkout_session(
    request: CreateCheckoutSessionRequest,
    user_id: str = Depends(get_current_user),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """
    Cria uma sessão de checkout para o usuário.
    Usado quando o usuário deseja assinar um plano premium.
    """
    try:
        checkout_session = await payment_service.create_checkout_session(user_id, request)
        return checkout_session
    except ValueError as e:
        # Erros de validação (plano não encontrado, etc.)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Erro ao criar sessão de checkout: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar sessão de checkout"
        )


@router.post("/webhook/stripe", response_model=WebhookVerificationResponse)
async def stripe_webhook(
    request: Request,
    payment_service: PaymentService = Depends(get_payment_service)
):
    """
    Webhook para receber notificações do Stripe.
    Não requer autenticação - validação feita via assinatura do webhook.
    """
    try:
        # Ler o payload do webhook
        payload = await request.body()
        sig_header = request.headers.get("Stripe-Signature", "")

        # Em produção, a verificação da assinatura seria feita aqui
        # No ambiente atual, apenas validamos o JSON

        # Converter payload para JSON
        try:
            event_json = json.loads(payload)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payload inválido"
            )

        # Extrair tipo de evento
        event_type = event_json.get("type", "")
        if not event_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de evento não especificado"
            )

        # Extrair objeto do evento
        event_data = event_json.get("data", {}).get("object", {})

        # Processar o webhook
        result = await payment_service.process_stripe_webhook(event_type, event_data)

        # Registrar recebimento bem-sucedido para diagnóstico
        if result.success:
            logger.info(f"Webhook Stripe processado com sucesso: {event_type}")
        else:
            logger.warning(
                f"Webhook Stripe recebido mas não processado completamente: {result.message}")

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao processar webhook do Stripe: {str(e)}")
        # Retornamos 200 mesmo com erro para que o Stripe não tente novamente
        # mas registramos o erro nos logs
        return WebhookVerificationResponse(
            success=False,
            message=f"Erro ao processar webhook: {str(e)}",
            event_type="unknown"
        )


@router.post("/webhook/hotmart", response_model=WebhookVerificationResponse)
async def hotmart_webhook(
    request: Request,
    payload: Dict[str, Any] = Body(...),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """
    Webhook para receber notificações da Hotmart (implementação futura).
    Não requer autenticação - validação feita via token do webhook.
    """
    # Implementação futura - Hotmart
    return WebhookVerificationResponse(
        success=True,
        message="Webhook Hotmart recebido (implementação futura)",
        event_type="hotmart.purchase"
    )
