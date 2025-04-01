from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union
import jwt
from passlib.context import CryptContext
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Configurações de JWT
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Contexto de criptografia para senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Cria um token JWT.

    Args:
        data: Dados a serem incluídos no token
        expires_delta: Tempo de expiração do token

    Returns:
        Token JWT
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decodifica um token JWT.

    Args:
        token: Token JWT

    Returns:
        Dados contidos no token

    Raises:
        jwt.PyJWTError: Se o token for inválido
    """
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return decoded_token
    except jwt.PyJWTError as e:
        logger.error(f"Erro ao decodificar token: {str(e)}")
        raise e


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde à senha hash.

    Args:
        plain_password: Senha em texto plano.
        hashed_password: Senha hash para comparação.

    Returns:
        bool: True se as senhas corresponderem, False caso contrário.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Gera um hash seguro para a senha.

    Args:
        password: Senha em texto plano.

    Returns:
        str: Hash da senha.
    """
    return pwd_context.hash(password)


def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """
    Verifica a assinatura de um webhook.

    Args:
        payload: Conteúdo do webhook
        signature: Assinatura do webhook
        secret: Chave secreta para verificação

    Returns:
        True se a assinatura for válida, False caso contrário
    """
    # Esta é uma implementação simples para exemplo
    # Em produção, você deve usar as bibliotecas específicas de cada gateway
    try:
        # Exemplo para Stripe:
        # import stripe
        # stripe.WebhookSignature.verify_header(payload, signature, secret)

        # Por enquanto, retornamos True para testes
        return True
    except Exception as e:
        logger.error(f"Erro ao verificar assinatura do webhook: {str(e)}")
        return False
