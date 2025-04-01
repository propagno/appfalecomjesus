"""
MS-ChatIA - Ponto de entrada do aplicativo

Este arquivo serve como ponto de entrada para o servidor Uvicorn,
importando a aplicação FastAPI do módulo app.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import datetime
import logging

app = FastAPI(
    title="MS-ChatIA API",
    description="API do Microsserviço de Chat com IA do FaleComJesus.",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/health")
async def health_check():
    logger.info("Health check acessado")
    return {
        "status": "healthy",
        "service": "ms-chatia",
        "timestamp": datetime.datetime.now().isoformat()
    }


@app.get("/api/health")
async def api_health_check():
    logger.info("API health check acessado")
    return {
        "status": "healthy",
        "service": "ms-chatia",
        "timestamp": datetime.datetime.now().isoformat()
    }


@app.get("/api/chat/health")
async def api_chat_health():
    logger.info("API chat health check acessado")
    return {
        "status": "healthy",
        "service": "ms-chatia",
        "timestamp": datetime.datetime.now().isoformat()
    }


@app.get("/api/v1/health")
async def api_v1_health():
    logger.info("API v1 health check acessado")
    return {
        "status": "healthy",
        "service": "ms-chatia",
        "timestamp": datetime.datetime.now().isoformat()
    }


@app.get("/api/v1/chat/health")
async def api_v1_chat_health():
    logger.info("API v1 chat health check acessado")
    return {
        "status": "healthy",
        "service": "ms-chatia",
        "timestamp": datetime.datetime.now().isoformat()
    }


@app.get("/api/chatia/health")
async def api_chatia_health():
    logger.info("API chatia health check acessado")
    return {
        "status": "healthy",
        "service": "ms-chatia",
        "timestamp": datetime.datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
