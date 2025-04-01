import logging
from typing import Any, Dict, Optional

from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


class BaseError(Exception):
    """
    Erro base do sistema.

    Responsável por:
    - Padronizar erros
    - Facilitar logging
    - Permitir tradução
    - Garantir rastreabilidade

    Attributes:
        message: Mensagem de erro
        code: Código interno
        status_code: Status HTTP
        details: Detalhes adicionais
    """

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Inicializa erro.

        Args:
            message: Mensagem de erro
            code: Código interno
            status_code: Status HTTP
            details: Detalhes adicionais
        """
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte para dicionário.

        Returns:
            Dict com dados do erro
        """
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details
            }
        }


class ValidationError(BaseError):
    """
    Erro de validação.

    Usado quando:
    - Dados inválidos
    - Formato incorreto
    - Valores não permitidos
    """

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Inicializa erro.

        Args:
            message: Mensagem de erro
            details: Detalhes adicionais
        """
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


class AuthenticationError(BaseError):
    """
    Erro de autenticação.

    Usado quando:
    - Credenciais inválidas
    - Token expirado
    - Usuário não encontrado
    """

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Inicializa erro.

        Args:
            message: Mensagem de erro
            details: Detalhes adicionais
        """
        super().__init__(
            message=message,
            code="AUTHENTICATION_ERROR",
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details
        )


class AuthorizationError(BaseError):
    """
    Erro de autorização.

    Usado quando:
    - Permissão negada
    - Acesso restrito
    - Recurso protegido
    """

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Inicializa erro.

        Args:
            message: Mensagem de erro
            details: Detalhes adicionais
        """
        super().__init__(
            message=message,
            code="AUTHORIZATION_ERROR",
            status_code=status.HTTP_403_FORBIDDEN,
            details=details
        )


class NotFoundError(BaseError):
    """
    Erro de recurso não encontrado.

    Usado quando:
    - Registro não existe
    - Página não encontrada
    - Rota inválida
    """

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Inicializa erro.

        Args:
            message: Mensagem de erro
            details: Detalhes adicionais
        """
        super().__init__(
            message=message,
            code="NOT_FOUND_ERROR",
            status_code=status.HTTP_404_NOT_FOUND,
            details=details
        )


class ConflictError(BaseError):
    """
    Erro de conflito.

    Usado quando:
    - Registro duplicado
    - Violação de unique
    - Estado inconsistente
    """

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Inicializa erro.

        Args:
            message: Mensagem de erro
            details: Detalhes adicionais
        """
        super().__init__(
            message=message,
            code="CONFLICT_ERROR",
            status_code=status.HTTP_409_CONFLICT,
            details=details
        )


class RateLimitError(BaseError):
    """
    Erro de limite excedido.

    Usado quando:
    - Muitas requisições
    - Limite diário
    - Cooldown ativo
    """

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Inicializa erro.

        Args:
            message: Mensagem de erro
            details: Detalhes adicionais
        """
        super().__init__(
            message=message,
            code="RATE_LIMIT_ERROR",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details=details
        )


class ServiceUnavailableError(BaseError):
    """
    Erro de serviço indisponível.

    Usado quando:
    - API externa fora
    - Banco indisponível
    - Sistema em manutenção
    """

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Inicializa erro.

        Args:
            message: Mensagem de erro
            details: Detalhes adicionais
        """
        super().__init__(
            message=message,
            code="SERVICE_UNAVAILABLE",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details
        )


class DatabaseError(BaseError):
    """
    Erro de banco de dados.

    Usado quando:
    - Falha na conexão
    - Erro na query
    - Violação de constraint
    """

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Inicializa erro.

        Args:
            message: Mensagem de erro
            details: Detalhes adicionais
        """
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class OpenAIError(BaseError):
    """
    Erro da API da OpenAI.

    Usado quando:
    - API Key inválida
    - Erro na requisição
    - Resposta inválida
    """

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Inicializa erro.

        Args:
            message: Mensagem de erro
            details: Detalhes adicionais
        """
        super().__init__(
            message=message,
            code="OPENAI_ERROR",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details
        )


def handle_exception(error: Exception) -> Dict[str, Any]:
    """
    Trata exceção genérica.

    Args:
        error: Exceção ocorrida

    Returns:
        Dict com erro formatado
    """
    # Log do erro
    logger.error(
        f"Error occurred: {str(error)}",
        exc_info=True
    )

    # Erro base do sistema
    if isinstance(error, BaseError):
        return error.to_dict()

    # Erro HTTP do FastAPI
    if isinstance(error, HTTPException):
        return {
            "error": {
                "code": "HTTP_ERROR",
                "message": error.detail,
                "details": {
                    "status_code": error.status_code
                }
            }
        }

    # Erro genérico
    return {
        "error": {
            "code": "INTERNAL_ERROR",
            "message": "Erro interno do servidor",
            "details": {
                "type": type(error).__name__,
                "message": str(error)
            }
        }
    }
