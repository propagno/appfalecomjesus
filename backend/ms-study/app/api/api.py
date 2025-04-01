from fastapi import APIRouter
import datetime
import logging

from app.api.routes import (
    certificates,
    progress,
    reflections,
    study_plans
)

# Configurar logger
logger = logging.getLogger(__name__)

api_router = APIRouter()

# Rota de health check para /api/study/health


@api_router.get("/study/health")
async def api_health_check():
    logger.info("API health check endpoint acessado")
    return {
        "status": "ok",
        "service": "ms-study",
        "timestamp": datetime.datetime.now().isoformat()
    }

# Incluir as rotas dos diferentes endpoints
api_router.include_router(
    study_plans.router, prefix="/study-plans", tags=["Planos de Estudo"])
api_router.include_router(
    progress.router, prefix="/progress", tags=["Progresso de Estudo"])
api_router.include_router(
    reflections.router, prefix="/reflections", tags=["Reflexões Pessoais"])
api_router.include_router(
    certificates.router, prefix="/certificates", tags=["Certificados de Conclusão"])
