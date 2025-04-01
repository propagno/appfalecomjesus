#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import os

# Configurar o módulo de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger("ms-bible")

# Configurações da aplicação
DEBUG = os.getenv("DEBUG", "0") == "1"
APP_TITLE = "FaleComJesus Bible API"
APP_DESCRIPTION = "API de acesso ao conteúdo bíblico do sistema FaleComJesus"
APP_VERSION = "0.1.0"

# Criar aplicação FastAPI
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    debug=DEBUG,
    docs_url="/api/bible/docs" if not DEBUG else "/docs",
    redoc_url="/api/bible/redoc" if not DEBUG else "/redoc",
    openapi_url="/api/bible/openapi.json" if not DEBUG else "/openapi.json",
)

# Configurar CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://frontend:3000",
    os.getenv("FRONTEND_URL", ""),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin for origin in origins if origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar e inicializar banco de dados
try:
    from app.infrastructure.database import init_db
    init_db()
except Exception as e:
    logger.error(f"Erro ao inicializar o banco de dados: {str(e)}")

# Adicionar rotas da API
try:
    from app.api.api import api_router
    app.include_router(api_router, prefix="/api/bible")
except Exception as e:
    logger.error(f"Erro ao incluir rotas da API: {str(e)}")

# Rota de health check (sempre disponível)


@app.get("/health", tags=["healthcheck"])
def health_check():
    return {
        "status": "healthy",
        "service": "ms-bible",
        "version": APP_VERSION,
        "timestamp": datetime.now().isoformat()
    }

# Eventos de inicialização


@app.on_event("startup")
def startup_event():
    logger.info("Starting up MS-Bible service...")
    logger.info("MS-Bible service started successfully")


@app.on_event("shutdown")
def shutdown_event():
    logger.info("Shutting down MS-Bible service...")

# Rota raiz para informações da API


@app.get("/", tags=["root"])
def read_root():
    return {
        "service": "FaleComJesus - Bible API",
        "version": APP_VERSION,
        "documentation": "/api/bible/docs"
    }

# Manipulador global de exceções


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erro não tratado: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Ocorreu um erro interno no servidor"}
    )

# Para iniciar direto pelo Python
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
