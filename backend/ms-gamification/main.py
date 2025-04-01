#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
from typing import Dict, Any

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.api.v1.api import api_router
from app.db.session import engine, SessionLocal
from app.db.base import Base

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("ms-gamification")

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para gerenciamento de gamificação do FaleComJesus",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Configurar CORS
origins = [
    settings.FRONTEND_URL,
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging de requisições


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # Processa a requisição
    try:
        response = await call_next(request)
        process_time = time.time() - start_time

        # Log da requisição
        logger.info(
            f"Request: {request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.3f}s"
        )

        return response
    except Exception as e:
        # Log de erro
        logger.error(
            f"Request: {request.method} {request.url.path} - "
            f"Error: {str(e)}"
        )
        raise

# Handler para erros de validação


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"]
        })

    logger.warning(f"Validation error: {errors}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors}
    )

# Handler para erros do SQLAlchemy


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database error: {str(exc)}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database error occurred. Please try again later."}
    )

# Rotas de health check


@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, Any]:
    """
    Endpoint para verificar a saúde do serviço
    """
    return {
        "status": "healthy",
        "service": "ms-gamification",
        "version": settings.VERSION
    }


@app.get("/health/db", tags=["Health"])
async def db_health_check() -> Dict[str, Any]:
    """
    Endpoint para verificar a saúde da conexão com o banco de dados
    """
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {
            "status": "healthy",
            "database": "connected",
            "service": "ms-gamification"
        }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "service": "ms-gamification",
            "error": str(e)
        }

# Incluir rotas da API
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
