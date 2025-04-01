from fastapi import APIRouter, status
import datetime
import logging

from app.api.v1.endpoints import chat

api_router = APIRouter()

# Configurar logger
logger = logging.getLogger(__name__)

# Rota de health check


@api_router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Endpoint de health check para o serviço.
    Não requer autenticação.
    """
    logger.info("Health check endpoint acessado")
    return {
        "status": "ok",
        "service": "ms-chatia",
        "timestamp": datetime.datetime.now().isoformat()
    }

# Incluir routers de endpoints específicos
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
