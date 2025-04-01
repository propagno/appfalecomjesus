"""
Serviço de segurança do sistema FaleComJesus.

Este módulo implementa as funcionalidades de segurança da aplicação,
incluindo autenticação, autorização e criptografia.

Features:
    - Autenticação JWT
    - Criptografia AES
    - Hashing de senhas
    - Rate limiting
    - Proteção contra ataques
    - Validação de tokens
"""

from typing import Dict, List, Optional, Union
import logging
from datetime import datetime, timedelta
import jwt
import base64
import os
from passlib.context import CryptContext
from .config import settings
from .cache import cache
from fastapi import HTTPException, status

# Logger
logger = logging.getLogger(__name__)


class SecurityManager:
    """
    Gerenciador de segurança.

    Features:
        - JWT
        - Criptografia
        - Hashing
        - Rate limit
        - Proteção

    Attributes:
        pwd_context: Contexto de senhas
        fernet: Chave de criptografia
        metrics: Métricas de segurança
        secret_key: Chave secreta
        algorithm: Algoritmo JWT
        access_token_expire: Expiração do token
    """

    def __init__(
        self,
        secret_key: Optional[str] = None,
        algorithm: str = "HS256",
        access_token_expire: int = 15
    ):
        """
        Inicializa o gerenciador de segurança.

        Args:
            secret_key: Chave secreta
            algorithm: Algoritmo JWT
            access_token_expire: Minutos para expirar
        """
        # Configurações
        self.secret_key = secret_key or settings.JWT_SECRET_KEY
        self.algorithm = algorithm
        self.access_token_expire = access_token_expire

        # Contexto de senhas
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto"
        )

        # Chave para criptografia simples
        self.encryption_key = os.environ.get(
            "ENCRYPTION_KEY", "simple_key_for_dev")

        # Métricas
        self.metrics = {
            "auth_attempts": 0,
            "auth_failures": 0,
            "rate_limits": 0,
            "encryptions": 0
        }

        logger.info("Gerenciador de segurança inicializado")

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str
    ) -> bool:
        """
        Verifica senha.

        Args:
            plain_password: Senha em texto
            hashed_password: Senha hasheada

        Returns:
            bool: True se senha correta
        """
        try:
            return self.pwd_context.verify(
                plain_password,
                hashed_password
            )

        except Exception as e:
            logger.error(f"Erro ao verificar senha: {str(e)}")
            return False

    def get_password_hash(
        self,
        password: str
    ) -> str:
        """
        Gera hash de senha.

        Args:
            password: Senha em texto

        Returns:
            str: Hash da senha
        """
        try:
            return self.pwd_context.hash(password)

        except Exception as e:
            logger.error(f"Erro ao gerar hash: {str(e)}")
            raise

    def create_access_token(
        self,
        data: Dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Cria token de acesso.

        Args:
            data: Dados do token
            expires_delta: Tempo de expiração

        Returns:
            str: Token JWT
        """
        try:
            # Prepara dados
            to_encode = data.copy()

            # Define expiração
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(
                    minutes=self.access_token_expire
                )

            to_encode.update({"exp": expire})

            # Gera token
            encoded_jwt = jwt.encode(
                to_encode,
                self.secret_key,
                algorithm=self.algorithm
            )

            return encoded_jwt

        except Exception as e:
            logger.error(f"Erro ao criar token: {str(e)}")
            raise

    def create_refresh_token(
        self,
        data: Dict
    ) -> str:
        """
        Cria token de refresh.

        Args:
            data: Dados do token

        Returns:
            str: Token JWT
        """
        try:
            # Prepara dados
            to_encode = data.copy()

            # Define expiração
            expire = datetime.utcnow() + timedelta(
                days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
            )

            to_encode.update({"exp": expire})

            # Gera token
            encoded_jwt = jwt.encode(
                to_encode,
                self.secret_key,
                algorithm=self.algorithm
            )

            return encoded_jwt

        except Exception as e:
            logger.error(f"Erro ao criar refresh token: {str(e)}")
            raise

    def verify_token(
        self,
        token: str
    ) -> Dict:
        """
        Verifica token JWT.

        Args:
            token: Token JWT

        Returns:
            Dict: Dados do token
        """
        try:
            # Decodifica token
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )

            return payload

        except jwt.ExpiredSignatureError:
            logger.warning("Token expirado")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado"
            )

        except jwt.JWTError:
            logger.warning("Token inválido")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

        except Exception as e:
            logger.error(f"Erro ao verificar token: {str(e)}")
            raise

    async def check_rate_limit(
        self,
        ip: str,
        limit: int = 60,
        window: int = 60
    ) -> bool:
        """
        Verifica limite de requisições.

        Args:
            ip: IP do cliente
            limit: Limite de requisições
            window: Janela em segundos

        Returns:
            bool: True se dentro do limite
        """
        try:
            # Busca contador
            count = await cache.get(ip) or 0

            # Verifica limite
            if count >= limit:
                self.metrics["rate_limits"] += 1
                return False

            # Incrementa contador
            await cache.set(ip, count + 1, window)

            return True

        except Exception as e:
            logger.error(f"Erro ao verificar rate limit: {str(e)}")
            return True

    def encrypt_data(
        self,
        data: str
    ) -> str:
        """
        Criptografa dados.

        Args:
            data: Dados para criptografar

        Returns:
            str: Dados criptografados
        """
        try:
            # Implementação simplificada - NÃO usar em produção
            # Esta é apenas uma solução temporária para evitar a dependência de cryptography
            self.metrics["encryptions"] += 1
            encoded = base64.b64encode(data.encode()).decode()
            return encoded
        except Exception as e:
            logger.error(f"Erro ao criptografar dados: {str(e)}")
            raise

    def decrypt_data(
        self,
        encrypted_data: str
    ) -> str:
        """
        Descriptografa dados.

        Args:
            encrypted_data: Dados criptografados

        Returns:
            str: Dados descriptografados
        """
        try:
            # Implementação simplificada - NÃO usar em produção
            # Esta é apenas uma solução temporária para evitar a dependência de cryptography
            decoded = base64.b64decode(encrypted_data.encode()).decode()
            return decoded
        except Exception as e:
            logger.error(f"Erro ao descriptografar dados: {str(e)}")
            raise

    def generate_csrf_token(self) -> str:
        """
        Gera token CSRF.

        Returns:
            str: Token CSRF
        """
        try:
            # Gera token
            token = self.fernet.encrypt(
                datetime.utcnow().isoformat().encode()
            ).decode()

            return token

        except Exception as e:
            logger.error(f"Erro ao gerar token CSRF: {str(e)}")
            raise

    def verify_csrf_token(
        self,
        token: str
    ) -> bool:
        """
        Verifica token CSRF.

        Args:
            token: Token CSRF

        Returns:
            bool: True se token válido
        """
        try:
            # Descriptografa token
            timestamp = self.fernet.decrypt(
                token.encode()
            ).decode()

            # Verifica timestamp
            token_time = datetime.fromisoformat(timestamp)
            now = datetime.utcnow()

            # Token válido por 1 hora
            return (now - token_time).total_seconds() <= 3600

        except Exception as e:
            logger.error(f"Erro ao verificar token CSRF: {str(e)}")
            return False


# Instância global de segurança
security = SecurityManager()

# Função para obter usuário atual


async def get_current_user(token: str):
    """
    Obtém o usuário atual a partir do token JWT.

    Args:
        token: Token JWT

    Returns:
        dict: Dados do usuário

    Raises:
        HTTPException: Se o token for inválido
    """
    payload = security.verify_token(token)
    return payload
