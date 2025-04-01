import logging
import httpx
from typing import Dict, Any, Optional, List
from fastapi import HTTPException, status
from app.core.config import settings

logger = logging.getLogger("auth_service")


class AuthService:
    """
    Serviço para integração com o MS-Auth
    """

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """
        Obtém informações de um usuário pelo email através da API do MS-Auth

        Args:
            email: Email do usuário

        Returns:
            Dicionário com dados do usuário ou None se não encontrado
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{settings.AUTH_SERVICE_URL}/api/v1/auth/users/by-email/{email}",
                    headers={
                        "Authorization": f"Bearer {settings.SERVICE_API_KEY}"
                    }
                )

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    logger.warning(
                        f"Usuário com email {email} não encontrado no MS-Auth")
                    return None
                else:
                    logger.error(
                        f"Erro ao buscar usuário no MS-Auth: {response.status_code} - {response.text}")
                    return None

        except Exception as e:
            logger.exception(f"Erro ao comunicar com MS-Auth: {str(e)}")
            return None

    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém informações de um usuário pelo ID através da API do MS-Auth

        Args:
            user_id: ID do usuário

        Returns:
            Dicionário com dados do usuário ou None se não encontrado
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{settings.AUTH_SERVICE_URL}/api/v1/auth/users/{user_id}",
                    headers={
                        "Authorization": f"Bearer {settings.SERVICE_API_KEY}"
                    }
                )

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    logger.warning(
                        f"Usuário com ID {user_id} não encontrado no MS-Auth")
                    return None
                else:
                    logger.error(
                        f"Erro ao buscar usuário no MS-Auth: {response.status_code} - {response.text}")
                    return None

        except Exception as e:
            logger.exception(f"Erro ao comunicar com MS-Auth: {str(e)}")
            return None

    @staticmethod
    async def update_user_subscription(user_id: str, subscription_data: Dict[str, Any]) -> bool:
        """
        Atualiza informações de assinatura de um usuário no MS-Auth

        Args:
            user_id: ID do usuário
            subscription_data: Dados da assinatura para atualização

        Returns:
            True se a atualização foi bem-sucedida, False caso contrário
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.put(
                    f"{settings.AUTH_SERVICE_URL}/api/v1/auth/subscription",
                    json={
                        "user_id": user_id,
                        "subscription_type": subscription_data.get("subscription_type", "free"),
                        "status": subscription_data.get("status", "active"),
                        "payment_gateway": subscription_data.get("payment_gateway"),
                        "expiration_date": subscription_data.get("expiration_date"),
                        "last_payment_date": subscription_data.get("last_payment_date")
                    },
                    headers={
                        "Authorization": f"Bearer {settings.SERVICE_API_KEY}"
                    }
                )

                if response.status_code in (200, 201):
                    logger.info(
                        f"Assinatura do usuário {user_id} atualizada no MS-Auth")
                    return True
                else:
                    logger.error(
                        f"Erro ao atualizar assinatura no MS-Auth: {response.status_code} - {response.text}")
                    return False

        except Exception as e:
            logger.exception(f"Erro ao comunicar com MS-Auth: {str(e)}")
            return False

    @staticmethod
    async def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verifica se um token JWT é válido através da API do MS-Auth

        Args:
            token: Token JWT a ser verificado

        Returns:
            Payload do token se válido, None caso contrário
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(
                    f"{settings.AUTH_SERVICE_URL}/api/v1/auth/verify-token",
                    json={"token": token},
                    headers={
                        "Authorization": f"Bearer {settings.SERVICE_API_KEY}"
                    }
                )

                data = response.json()
                if response.status_code == 200 and data.get("valid"):
                    return data.get("payload")
                else:
                    logger.warning(
                        f"Token inválido ou expirado: {response.status_code}")
                    return None

        except Exception as e:
            logger.exception(f"Erro ao verificar token com MS-Auth: {str(e)}")
            return None
