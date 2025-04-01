import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time

from app.core.config import get_settings
from app.api.v1.routes import api_router
from app.infrastructure.database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("main")

settings = get_settings()

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para gerenciamento de planos de estudo bíblico",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log requests and responses."""
    start_time = time.time()

    # Process the request
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        # Log the request
        logger.info(
            f"Request: {request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Time: {process_time:.4f}s"
        )

        return response
    except Exception as e:
        # Log the error
        logger.error(
            f"Request failed: {request.method} {request.url.path} | "
            f"Error: {str(e)}"
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Health check endpoint


@app.get("/health")
async def health_check():
    """
    Endpoint para verificar a saúde do serviço
    """
    return {"status": "healthy", "version": settings.VERSION}

# Initialize database on startup


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Initializing database")
    init_db()
    logger.info(f"Application {settings.APP_NAME} started")

# Run app with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8004, reload=True)
