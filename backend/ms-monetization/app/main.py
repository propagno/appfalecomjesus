import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.core.config import settings

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    description="API do serviço de monetização do FaleComJesus",
    version=settings.VERSION,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "http://127.0.0.1:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas da API
app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    """
    Rota raiz do serviço de monetização.
    """
    return {
        "message": "MS-Monetization API",
        "docs": f"{settings.API_PREFIX}/docs",
    }


@app.get("/health")
async def health_check():
    """
    Verifica a saúde do serviço de monetização.
    """
    return {
        "status": "ok",
        "service": "ms-monetization",
        "version": "0.1.0",
    }


@app.get("/api/monetization/health")
async def api_health_check():
    """
    Endpoint de saúde para acesso via NGINX (compatibilidade).
    """
    return {
        "status": "ok",
        "service": "ms-monetization",
        "version": "0.1.0",
    }

# Inicialização do serviço


@app.on_event("startup")
async def startup_event():
    logger.info("Iniciando o serviço de monetização...")

# Finalização do serviço


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Finalizando o serviço de monetização...")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
