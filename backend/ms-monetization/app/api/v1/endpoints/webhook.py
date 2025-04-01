from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.webhook import WebhookService
import logging

router = APIRouter()
logger = logging.getLogger("webhook")


@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Endpoint para receber webhooks do Stripe.

    Args:
        request: Requisição HTTP
        db: Sessão do banco de dados

    Returns:
        dict: Resposta de sucesso ou erro
    """
    # Obtém o payload e a assinatura do webhook
    payload = await request.body()
    signature = request.headers.get("stripe-signature")

    if not signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assinatura do webhook não fornecida"
        )

    # Processa o webhook
    success, error_message = await WebhookService.handle_stripe_webhook(
        db,
        payload,
        signature
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )

    return {"status": "success"}


@router.post("/hotmart")
async def hotmart_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Endpoint para receber webhooks do Hotmart.

    Args:
        request: Requisição HTTP
        db: Sessão do banco de dados

    Returns:
        dict: Resposta de sucesso ou erro
    """
    try:
        # Obtém o payload do webhook
        payload = await request.json()
        logger.info(f"Webhook Hotmart recebido: {payload}")

        # Processa o webhook
        success, error_message = await WebhookService.handle_hotmart_webhook(
            db,
            payload
        )

        if not success:
            logger.error(f"Erro ao processar webhook Hotmart: {error_message}")
            # Não retornar erro para evitar reenvios do Hotmart
            return {"status": "received", "message": error_message}

        return {"status": "success"}
    except Exception as e:
        logger.exception(f"Exceção ao processar webhook Hotmart: {str(e)}")
        # Não retornar erro para evitar reenvios do Hotmart
        return {"status": "received", "error": str(e)}
