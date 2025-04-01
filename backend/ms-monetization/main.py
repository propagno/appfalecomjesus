import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.api import api_router
from app.core.config import settings

# Criação da aplicação FastAPI com metadados para documentação
app = FastAPI(
    title="MS-Monetization API",
    description="""
    Microsserviço de Monetização para o sistema FaleComJesus
    
    Funcionalidades:
    
    * Gerenciamento de Assinaturas (Free/Premium)
    * Processamento de Webhooks de gateways de pagamento (Stripe/Hotmart)
    * Controle de limites de uso para usuários Free
    * Recompensas por visualização de anúncios
    """,
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    openapi_tags=[
        {
            "name": "Subscriptions",
            "description": "Endpoints para gerenciamento de assinaturas Premium/Free",
        },
        {
            "name": "Webhooks",
            "description": "Webhooks para recebimento de eventos de pagamento (Stripe/Hotmart)",
        },
        {
            "name": "Payment",
            "description": "Endpoints para gerenciamento de pagamentos",
        },
        {
            "name": "Ad Rewards",
            "description": "Recompensas por visualização de anúncios para usuários Free",
        },
        {
            "name": "chat-limits",
            "description": "Gerenciamento de limites de mensagens no chat para usuários Free",
        },
    ],
)

# Configuração de CORS para comunicação segura com o frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração de sessão para autenticação
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    max_age=settings.SESSION_MAX_AGE,
)

# Inclusão das rotas da API
app.include_router(api_router, prefix=settings.API_V1_STR)

# Rota raiz para verificação de saúde do serviço


@app.get("/", tags=["Health Check"])
async def health_check():
    """
    Verifica se o serviço está operacional.

    Retorna:
        dict: Status do serviço e versão da API
    """
    return {
        "status": "ok",
        "service": "ms-monetization",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG_MODE
    )
