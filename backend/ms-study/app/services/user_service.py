import uuid
import logging
import httpx
from typing import Optional, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)


class UserService:
    """
    Serviço para buscar informações do usuário a partir do MS-Auth.

    Este serviço facilita a obtenção de detalhes de usuário para exibir nos certificados 
    e outras funcionalidades que precisam dos dados do usuário.
    """

    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """
        Busca informações do usuário no MS-Auth pelo ID.

        Args:
            user_id: ID do usuário a ser consultado.

        Returns:
            Dicionário com as informações do usuário ou None se não encontrado.
        """
        try:
            auth_service_url = f"{settings.AUTH_SERVICE_URL}/api/users/{user_id}"

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    auth_service_url,
                    headers={"Service-Auth-Key": settings.SERVICE_AUTH_KEY},
                    timeout=10.0
                )

                if response.status_code == 200:
                    user_data = response.json()
                    logger.info(
                        f"Dados do usuário {user_id} obtidos com sucesso do MS-Auth")
                    return user_data
                elif response.status_code == 404:
                    logger.warning(
                        f"Usuário {user_id} não encontrado no MS-Auth")
                    return None
                else:
                    logger.error(
                        f"Erro ao buscar usuário {user_id} no MS-Auth: {response.status_code} - {response.text}")
                    return None

        except Exception as e:
            logger.exception(
                f"Exceção ao buscar usuário {user_id} no MS-Auth: {str(e)}")
            return None

    async def get_user_name(self, user_id: uuid.UUID) -> str:
        """
        Obtém apenas o nome do usuário para uso em certificados.

        Args:
            user_id: ID do usuário.

        Returns:
            Nome do usuário ou "Usuário" se não for possível obter o nome.
        """
        user_data = await self.get_user_by_id(user_id)

        if user_data and "name" in user_data:
            return user_data["name"]

        return "Usuário"  # Valor padrão se não conseguir obter o nome
