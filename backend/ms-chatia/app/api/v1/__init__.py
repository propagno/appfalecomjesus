from fastapi import APIRouter
from app.api.v1.endpoints.chat import router as chat_router

# Criar router principal da API v1
api_router = APIRouter()

# Incluir todos os sub-routers com prefixos específicos
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
