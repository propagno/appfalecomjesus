from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger("ms-admin")

# App FastAPI
app = FastAPI(
    title="FaleComJesus Admin API",
    description="API de administração do sistema FaleComJesus",
    version="0.1.0",
)

# Configuração de CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://frontend:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas


@app.get("/")
def read_root():
    return {"message": "Admin API", "version": "0.1.0"}


@app.get("/api/v1/admin/health")
def health_check():
    return {"status": "healthy", "service": "ms-admin", "timestamp": datetime.now().isoformat()}


@app.get("/api/v1/admin/metrics")
def get_metrics():
    # Este é um endpoint placeholder - em uma implementação real
    # você buscaria métricas de outros microsserviços ou banco de dados
    return {
        "users": {
            "total": 100,
            "active": 85,
            "premium": 35
        },
        "studies": {
            "active_plans": 72,
            "completed_plans": 45
        },
        "chat": {
            "messages_today": 345,
            "average_per_user": 5.2
        }
    }
