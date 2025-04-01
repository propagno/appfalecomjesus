from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import logging
import traceback
from datetime import datetime

# Configuração de logging estruturado
logger = logging.getLogger(__name__)


class AppError(Exception):
    """
    Classe base para erros da aplicação
    """

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or "INTERNAL_ERROR"
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(AppError):
    """
    Erro de validação de dados
    """

    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="VALIDATION_ERROR",
            details=details
        )


class AuthenticationError(AppError):
    """
    Erro de autenticação
    """

    def __init__(self, message: str = "Não autorizado"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="AUTHENTICATION_ERROR"
        )


class RateLimitError(AppError):
    """
    Erro de limite de taxa excedido
    """

    def __init__(self, message: str = "Limite de requisições excedido"):
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_ERROR"
        )


class BusinessError(AppError):
    """
    Erro de regra de negócio
    """

    def __init__(self, message: str, error_code: str = "BUSINESS_ERROR"):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code=error_code
        )


async def error_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler global de erros
    """
    # Preparar dados do erro
    timestamp = datetime.utcnow().isoformat()
    error_id = str(hash(timestamp))

    # Dados base da resposta
    error_response = {
        "error": {
            "id": error_id,
            "timestamp": timestamp,
            "path": request.url.path
        }
    }

    # Se for um erro da aplicação
    if isinstance(exc, AppError):
        error_response["error"].update({
            "code": exc.error_code,
            "message": exc.message,
            "details": exc.details
        })
        status_code = exc.status_code

        # Log estruturado do erro
        logger.error(
            f"Application error: {exc.error_code}",
            extra={
                "error_id": error_id,
                "error_code": exc.error_code,
                "status_code": status_code,
                "path": request.url.path,
                "details": exc.details
            }
        )

    # Se for um erro não tratado
    else:
        error_response["error"].update({
            "code": "INTERNAL_ERROR",
            "message": "Erro interno do servidor"
        })
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        # Log detalhado do erro não tratado
        logger.error(
            "Unhandled error",
            extra={
                "error_id": error_id,
                "error_type": type(exc).__name__,
                "error_message": str(exc),
                "traceback": traceback.format_exc(),
                "path": request.url.path
            }
        )

        # Em desenvolvimento, incluir stack trace
        if request.app.debug:
            error_response["error"]["debug"] = {
                "type": type(exc).__name__,
                "message": str(exc),
                "traceback": traceback.format_exc()
            }

    return JSONResponse(
        status_code=status_code,
        content=error_response
    )


def setup_error_handlers(app):
    """
    Configura os handlers de erro na aplicação
    """
    app.add_exception_handler(AppError, error_handler)
    app.add_exception_handler(Exception, error_handler)

    logger.info("Error handlers configured successfully")
