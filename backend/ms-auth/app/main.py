from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
import os
from .api.v1.auth.routes import router as auth_router
from .core.config import get_settings
from .infrastructure.db_init import init_db
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ms-auth")

settings = get_settings()

app = FastAPI(
    title="Auth Microservice API",
    description="Authentication Microservice for FaleComJesus",
    version="0.1.0",
    docs_url="/api/v1/auth/docs",
    redoc_url="/api/v1/auth/redoc",
    openapi_url="/api/v1/auth/openapi.json",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para processar diferentes tipos de content-type


@app.middleware("http")
async def content_type_middleware(request: Request, call_next):
    """
    Middleware para garantir compatibilidade com diferentes 
    tipos de Content-Type, especialmente para o endpoint de login.
    """
    path = request.url.path
    original_content_type = request.headers.get("Content-Type", "")

    # Verificar se é uma solicitação POST para o endpoint de login
    if (path.endswith("/login") and request.method == "POST"):
        logger.info(
            f"Login request with Content-Type: {original_content_type}")

        # Se o cliente enviar como JSON mas o backend espera form
        if "application/json" in original_content_type.lower():
            try:
                # Lê o corpo JSON
                json_body = await request.json()

                # Define as credenciais no state para uso posterior
                request.state.credentials = json_body
                logger.info("Processed JSON credentials for login")
            except Exception as e:
                logger.error(f"Error processing login request: {str(e)}")
                pass

    response = await call_next(request)
    return response

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth")

# Add compatibility routes for old /api/auth pattern
compat_router = auth_router
app.include_router(auth_router, prefix="/api/auth")

# Add app state
app.state.settings = settings


@app.get("/api/v1/auth/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "service": "ms-auth"}


# Compatibility health check endpoint
@app.get("/api/auth/health")
def health_check_compat():
    """
    Compatibility health check endpoint.
    """
    return {"status": "healthy", "service": "ms-auth"}


@app.on_event("startup")
def startup_event():
    """Initialize the database on startup."""
    init_db()
    logger.info("MS-Auth service started and database initialized")
