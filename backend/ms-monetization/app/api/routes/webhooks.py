from fastapi import APIRouter, Request, Response, Depends, Header, HTTPException, status
from app.api.deps import get_subscription_service
from app.services.subscription_service import SubscriptionService
from app.services.webhook_service import WebhookService
from app.core.config import settings
from app.core.security import verify_webhook_signature
import logging
import json
from typing import Dict, Any

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/stripe",
    summary="Webhook do Stripe",
    description="""
    Endpoint para receber notificações de eventos do Stripe.
    
    Este webhook processa eventos como pagamentos confirmados, assinaturas criadas, 
    canceladas ou atualizadas, e falhas de pagamento. Cada tipo de evento resulta
    em uma ação específica no sistema, como ativar ou cancelar uma assinatura.
    
    O endpoint verifica a assinatura do Stripe para garantir que a requisição é autêntica,
    utilizando o header 'Stripe-Signature' e a chave secreta configurada.
    
    **Importante**: Este endpoint sempre retorna status 200, mesmo em caso de erro interno,
    para evitar que o Stripe continue tentando reenviar o webhook.
    """,
    responses={
        200: {
            "description": "Webhook processado (com ou sem erros)",
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Processamento bem-sucedido",
                            "value": {"status": "success", "message": "Assinatura criada com sucesso para o usuário abc123"}
                        },
                        "error": {
                            "summary": "Erro no processamento",
                            "value": {"status": "error", "message": "Usuário não encontrado"}
                        }
                    }
                }
            }
        },
        401: {
            "description": "Assinatura do webhook inválida",
            "content": {
                "application/json": {
                    "example": {"detail": "Assinatura inválida"}
                }
            }
        }
    }
)
async def stripe_webhook(
    request: Request,
    signature: str = Header(None, alias="Stripe-Signature",
                            description="Assinatura do webhook do Stripe para verificação de autenticidade"),
    subscription_service: SubscriptionService = Depends(
        get_subscription_service)
) -> Dict[str, Any]:
    """
    Webhook para eventos do Stripe.
    """
    logger.info("Recebendo webhook do Stripe")

    # Ler o corpo da requisição
    body = await request.body()

    # Verificar a assinatura do Stripe
    if settings.STRIPE_WEBHOOK_SECRET:
        if not verify_webhook_signature(body, signature, settings.STRIPE_WEBHOOK_SECRET):
            logger.warning("Assinatura inválida do webhook do Stripe")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Assinatura inválida"
            )

    # Processar o webhook
    try:
        # Parsear o JSON
        payload = json.loads(body)

        # Criar instância do WebhookService e processar o evento
        webhook_service = WebhookService(subscription_service)
        result = await webhook_service.process_stripe_webhook(payload)

        return {"status": "success", "message": result}
    except Exception as e:
        logger.error(f"Erro ao processar webhook do Stripe: {str(e)}")
        # Importante: sempre retornar 200 mesmo em caso de erro para o Stripe não continuar tentando
        return Response(
            content=json.dumps({"status": "error", "message": str(e)}),
            status_code=200,
            media_type="application/json"
        )


@router.post(
    "/hotmart",
    summary="Webhook do Hotmart",
    description="""
    Endpoint para receber notificações de eventos do Hotmart.
    
    Este webhook processa eventos como compras aprovadas, assinaturas canceladas, 
    boletos pagos, e reembolsos. Cada evento resulta em uma ação correspondente
    no sistema, como ativar uma assinatura premium ou registrar um cancelamento.
    
    O endpoint valida a autenticidade da requisição verificando o header 'X-Hotmart-Signature'
    contra a chave secreta configurada.
    
    **Importante**: Este endpoint sempre retorna status 200, mesmo em caso de erro,
    para evitar que o Hotmart continue tentando reenviar o webhook.
    """,
    responses={
        200: {
            "description": "Webhook processado (com ou sem erros)",
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Processamento bem-sucedido",
                            "value": {"status": "success", "message": "Assinatura ativada para o usuário xyz789"}
                        },
                        "error": {
                            "summary": "Erro no processamento",
                            "value": {"status": "error", "message": "Email não cadastrado no sistema"}
                        }
                    }
                }
            }
        },
        401: {
            "description": "Assinatura do webhook inválida",
            "content": {
                "application/json": {
                    "example": {"detail": "Assinatura inválida"}
                }
            }
        }
    }
)
async def hotmart_webhook(
    request: Request,
    signature: str = Header(None, alias="X-Hotmart-Signature",
                            description="Assinatura do webhook do Hotmart para verificação de autenticidade"),
    subscription_service: SubscriptionService = Depends(
        get_subscription_service)
) -> Dict[str, Any]:
    """
    Webhook para eventos do Hotmart.
    """
    logger.info("Recebendo webhook do Hotmart")

    # Ler o corpo da requisição
    body = await request.body()

    # Verificar a assinatura do Hotmart
    if settings.HOTMART_WEBHOOK_SECRET:
        if not verify_webhook_signature(body, signature, settings.HOTMART_WEBHOOK_SECRET):
            logger.warning("Assinatura inválida do webhook do Hotmart")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Assinatura inválida"
            )

    # Processar o webhook
    try:
        # Parsear o JSON
        payload = json.loads(body)

        # Criar instância do WebhookService e processar o evento
        webhook_service = WebhookService(subscription_service)
        result = await webhook_service.process_hotmart_webhook(payload)

        return {"status": "success", "message": result}
    except Exception as e:
        logger.error(f"Erro ao processar webhook do Hotmart: {str(e)}")
        # Sempre retornar 200 para o Hotmart não continuar tentando
        return Response(
            content=json.dumps({"status": "error", "message": str(e)}),
            status_code=200,
            media_type="application/json"
        )
