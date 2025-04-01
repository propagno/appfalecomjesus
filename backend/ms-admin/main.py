from app.db.session import create_tables
from app.api.api import api_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime
import os

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger("ms-admin")

# Configurações da aplicação
DEBUG = os.getenv("DEBUG", "0") == "1"
APP_TITLE = "FaleComJesus Admin API"
APP_DESCRIPTION = "API de administração do sistema FaleComJesus"
APP_VERSION = "0.1.0"

# Inicialização do FastAPI
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    debug=DEBUG,
    docs_url="/api/admin/docs" if not DEBUG else "/docs",
    redoc_url="/api/admin/redoc" if not DEBUG else "/redoc",
    openapi_url="/api/admin/openapi.json" if not DEBUG else "/openapi.json",
)

# Configuração de CORS
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

# Importar e incluir as rotas da API
app.include_router(api_router, prefix="/api/admin")

# Rota para verificação de saúde


@app.get("/health", tags=["healthcheck"])
def health_check():
    return {
        "status": "healthy",
        "service": "ms-admin",
        "version": APP_VERSION,
        "timestamp": datetime.now().isoformat()
    }


# Inicialização do banco de dados


@app.on_event("startup")
def startup_event():
    logger.info("Starting up MS-Admin service...")

    # Criar tabelas do banco de dados se não existirem
    try:
        create_tables()
        logger.info("Database tables created/verified successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")

    logger.info("MS-Admin service started successfully")


@app.on_event("shutdown")
def shutdown_event():
    logger.info("Shutting down MS-Admin service...")

# Rota raiz para informações da API


@app.get("/", tags=["root"])
def read_root():
    return {
        "service": "FaleComJesus - Admin API",
        "version": APP_VERSION,
        "documentation": "/api/admin/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
