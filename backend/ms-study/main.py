import logging
from typing import Dict
import datetime

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Alterar o import para a estrutura correta da API
from app.api.api import api_router
from app.core.config import settings
from app.db.session import SessionLocal

# Configurar logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MS-Study API",
    description="Microsserviço para gerenciamento dos planos de estudos e progresso dos usuários.",
    version="0.1.0",
)

# Configurar CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Função para obter a sessão do banco de dados


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota de saúde


@app.get("/health")
def health_check():
    logger.info("Health check endpoint acessado")
    return {
        "status": "ok",
        "timestamp": datetime.datetime.now().isoformat()
    }

# Rota raiz


@app.get("/")
def read_root():
    logger.info("Root endpoint acessado")
    return {"message": "Welcome to MS-Study API"}


# Incluir as rotas da API
app.include_router(api_router, prefix="/api")

# Se for executado diretamente, iniciar o servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
