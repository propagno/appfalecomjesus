import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
from uuid import UUID

import httpx
from fastapi import HTTPException, status

from app.core.config import settings

logger = logging.getLogger(__name__)


class HotmartService:
    """
    Serviço para integração com Hotmart.

    Responsável por:
    - Criar links de checkout
    - Processar webhooks de pagamento
    - Gerenciar assinaturas
    - Controlar acessos

    Attributes:
        base_url: URL base da API do Hotmart
        client_id: ID do cliente na plataforma
        client_secret: Chave secreta do cliente
    """

    def __init__(self):
        """
        Inicializa o serviço do Hotmart.

        Configura credenciais e URLs base.
        """
        self.base_url = settings.HOTMART_BASE_URL
        self.client_id = settings.HOTMART_CLIENT_ID
        self.client_secret = settings.HOTMART_CLIENT_SECRET

    async def get_access_token(self) -> str:
        """
        Obtém token de acesso OAuth2.

        Returns:
            Token de acesso

        Raises:
            HTTPException: Se erro na autenticação
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/oauth/token",
                    data={
                        "grant_type": "client_credentials",
                        "client_id": self.client_id,
                        "client_secret": self.client_secret
                    }
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Erro de autenticação no Hotmart"
                    )

                data = response.json()
                return data["access_token"]

        except httpx.HTTPError as e:
            logger.error(f"Hotmart auth error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao autenticar no Hotmart"
            )

    async def create_checkout_url(
        self,
        user_id: UUID,
        plan_id: UUID,
        amount: int
    ) -> Dict:
        """
        Cria URL de checkout para pagamento.

        Args:
            user_id: ID do usuário
            plan_id: ID do plano
            amount: Valor em centavos

        Returns:
            Dict com URL e ID da transação

        Raises:
            HTTPException: Se erro na criação
        """
        try:
            token = await self.get_access_token()

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/payments/checkout",
                    headers={"Authorization": f"Bearer {token}"},
                    json={
                        "product_id": settings.HOTMART_PRODUCT_ID,
                        "price": amount / 100,  # Converte centavos para reais
                        "currency": "BRL",
                        "customer": {
                            "email": str(user_id)  # Usado para rastreamento
                        },
                        "custom_fields": {
                            "user_id": str(user_id),
                            "plan_id": str(plan_id)
                        }
                    }
                )

                if response.status_code != 201:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Erro ao criar checkout no Hotmart"
                    )

                data = response.json()
                return {
                    "url": data["checkout_url"],
                    "transaction_id": data["transaction_id"],
                    "amount": amount,
                    "status": "pending"
                }

        except httpx.HTTPError as e:
            logger.error(f"Hotmart checkout error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar checkout"
            )

    async def verify_webhook_signature(
        self,
        payload: bytes,
        signature: str
    ) -> bool:
        """
        Verifica assinatura do webhook Hotmart.

        Args:
            payload: Dados do webhook
            signature: Assinatura do Hotmart

        Returns:
            True se assinatura válida

        Raises:
            HTTPException: Se assinatura inválida
        """
        try:
            # Implementar verificação de assinatura HMAC
            # Hotmart usa SHA-256 com secret
            return True  # TODO: implementar verificação real

        except Exception as e:
            logger.error(f"Webhook verification error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assinatura do webhook inválida"
            )

    async def cancel_subscription(
        self,
        subscription_id: str
    ) -> None:
        """
        Cancela assinatura no Hotmart.

        Args:
            subscription_id: ID da assinatura

        Raises:
            HTTPException: Se erro no cancelamento
        """
        try:
            token = await self.get_access_token()

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/subscriptions/{subscription_id}/cancel",
                    headers={"Authorization": f"Bearer {token}"}
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Erro ao cancelar assinatura no Hotmart"
                    )

        except httpx.HTTPError as e:
            logger.error(f"Hotmart cancel error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao cancelar assinatura"
            )

    async def refund_payment(
        self,
        transaction_id: str
    ) -> None:
        """
        Processa reembolso de pagamento.

        Args:
            transaction_id: ID da transação

        Raises:
            HTTPException: Se erro no reembolso
        """
        try:
            token = await self.get_access_token()

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/payments/{transaction_id}/refund",
                    headers={"Authorization": f"Bearer {token}"}
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Erro ao reembolsar pagamento no Hotmart"
                    )

        except httpx.HTTPError as e:
            logger.error(f"Hotmart refund error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao processar reembolso"
            )

    async def get_subscription_details(
        self,
        subscription_id: str
    ) -> Optional[Dict]:
        """
        Retorna detalhes da assinatura.

        Args:
            subscription_id: ID da assinatura

        Returns:
            Dict com detalhes ou None

        Raises:
            HTTPException: Se erro na busca
        """
        try:
            token = await self.get_access_token()

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/subscriptions/{subscription_id}",
                    headers={"Authorization": f"Bearer {token}"}
                )

                if response.status_code == 404:
                    return None

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Erro ao buscar assinatura no Hotmart"
                    )

                data = response.json()
                return {
                    "id": data["id"],
                    "status": data["status"],
                    "plan": data["plan"],
                    "created_at": data["created_at"],
                    "next_payment": data["next_payment_date"],
                    "payment_method": data["payment_method"]
                }

        except httpx.HTTPError as e:
            logger.error(f"Hotmart subscription error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao buscar assinatura"
            )
