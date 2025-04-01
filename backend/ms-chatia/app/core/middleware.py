"""
Serviço de middleware do sistema FaleComJesus.

Este módulo implementa os middlewares da aplicação,
incluindo autenticação, CORS, rate limiting e logging.

Features:
    - Autenticação JWT
    - CORS configurável
    - Rate limiting
    - Logging de requisições
    - Compressão GZIP
    - Headers de segurança
"""

from typing import List, Optional, Dict, Any
import time
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from .config import settings
from .security import security
from .logging import logger


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware de autenticação.

    Features:
        - Validação JWT
        - Rotas públicas
        - Refresh token
        - Rate limiting

    Attributes:
        public_routes: Lista de rotas públicas
    """

    def __init__(
        self,
        app: FastAPI,
        public_routes: Optional[List[str]] = None
    ):
        """
        Inicializa o middleware.

        Args:
            app: Aplicação FastAPI
            public_routes: Rotas públicas
        """
        super().__init__(app)
        self.public_routes = public_routes or [
            # Autenticação
            "/api/auth/login",
            "/api/auth/register",
            "/api/auth/refresh",

            # Documentação
            "/docs",
            "/redoc",
            "/openapi.json",

            # Health Check
            "/health",
            "/api/health",
            "/api/v1/health",
            "/api/v1/chat/health",
            "/api/chat/health",

            # Static
            "/favicon.ico",
            "/robots.txt",

            # Páginas públicas da documentação Swagger
            "/docs/oauth2-redirect",
            "/swagger-ui-bundle.js",
            "/swagger-ui.css"
        ]

    async def dispatch(
        self,
        request: Request,
        call_next
    ) -> Response:
        """
        Processa a requisição.

        Args:
            request: Requisição
            call_next: Próximo middleware

        Returns:
            Response: Resposta

        Raises:
            HTTPException: Não autorizado
        """
        try:
            # Verifica rota pública
            path = request.url.path
            if any(path.startswith(public_route) for public_route in self.public_routes if public_route.endswith('*')) or path in self.public_routes:
                return await call_next(request)

            # Verifica token
            token = request.cookies.get("access_token")
            if not token:
                raise HTTPException(
                    status_code=401,
                    detail="Token não fornecido"
                )

            # Valida token
            payload = security.verify_token(token)

            # Rate limit
            if not await security.check_rate_limit(
                request.client.host
            ):
                raise HTTPException(
                    status_code=429,
                    detail="Muitas requisições"
                )

            # Adiciona usuário
            request.state.user = payload

            # Próximo
            return await call_next(request)

        except Exception as e:
            logger.error(f"Erro no auth middleware: {str(e)}")
            raise


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware de logging.

    Features:
        - Log de requisições
        - Tempo de processamento
        - Erros
        - Métricas

    Attributes:
        metrics: Métricas de requisições
    """

    def __init__(self, app: FastAPI):
        """
        Inicializa o middleware.

        Args:
            app: Aplicação FastAPI
        """
        super().__init__(app)
        self.metrics = {
            "total": 0,
            "success": 0,
            "error": 0,
            "avg_time": 0
        }

    async def dispatch(
        self,
        request: Request,
        call_next
    ) -> Response:
        """
        Processa a requisição.

        Args:
            request: Requisição
            call_next: Próximo middleware

        Returns:
            Response: Resposta
        """
        try:
            # Início
            start_time = time.time()

            # Próximo
            response = await call_next(request)

            # Tempo
            process_time = time.time() - start_time

            # Log
            await logger.info(
                f"{request.method} {request.url.path}",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "status": response.status_code,
                    "time": process_time
                }
            )

            # Métricas
            self.metrics["total"] += 1
            if response.status_code < 400:
                self.metrics["success"] += 1
            else:
                self.metrics["error"] += 1

            self.metrics["avg_time"] = (
                (self.metrics["avg_time"] * (self.metrics["total"] - 1) +
                 process_time) / self.metrics["total"]
            )

            return response

        except Exception as e:
            logger.error(f"Erro no logging middleware: {str(e)}")
            raise


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Middleware de segurança.

    Features:
        - Headers de segurança
        - Proteção contra ataques
        - CORS
        - CSP

    Attributes:
        headers: Headers de segurança
    """

    def __init__(self, app: FastAPI):
        """
        Inicializa o middleware.

        Args:
            app: Aplicação FastAPI
        """
        super().__init__(app)
        self.headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'"
        }

    async def dispatch(
        self,
        request: Request,
        call_next
    ) -> Response:
        """
        Processa a requisição.

        Args:
            request: Requisição
            call_next: Próximo middleware

        Returns:
            Response: Resposta
        """
        try:
            # Próximo
            response = await call_next(request)

            # Adiciona headers
            for key, value in self.headers.items():
                response.headers[key] = value

            return response

        except Exception as e:
            logger.error(f"Erro no security middleware: {str(e)}")
            raise


def setup_middleware(app: FastAPI) -> None:
    """
    Configura os middlewares.

    Args:
        app: Aplicação FastAPI
    """
    try:
        # CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )

        # GZIP
        app.add_middleware(GZipMiddleware)

        # Autenticação
        app.add_middleware(AuthMiddleware)

        # Logging
        app.add_middleware(LoggingMiddleware)

        # Segurança
        app.add_middleware(SecurityMiddleware)

    except Exception as e:
        logger.error(f"Erro ao configurar middlewares: {str(e)}")
        raise


# Alias para a função com 's' (compatibilidade com main.py)
setup_middlewares = setup_middleware
