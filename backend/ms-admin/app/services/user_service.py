import httpx
import os
from typing import Dict, Any, List, Optional
import logging
from ..schemas.auth import User

# URL do microsserviço de autenticação
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://ms-auth:5000")

logger = logging.getLogger("ms-admin")


async def get_users(
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_premium: Optional[bool] = None,
    sort_by: str = "created_at",
    sort_desc: bool = True
) -> Dict[str, Any]:
    """
    Obtém lista de usuários do sistema com filtros e paginação

    Args:
        skip: Número de registros para pular (para paginação)
        limit: Número máximo de registros a retornar
        search: Filtro de texto para nome/email
        is_active: Filtro para usuários ativos/inativos
        is_premium: Filtro para usuários premium
        sort_by: Campo para ordenação
        sort_desc: Se True, ordena de forma descendente

    Returns:
        Dict contendo lista de usuários e total
    """
    try:
        # Constrói parâmetros de consulta
        params = {
            "skip": skip,
            "limit": limit,
            "sort_by": sort_by,
            "sort_desc": "true" if sort_desc else "false"
        }

        if search:
            params["search"] = search
        if is_active is not None:
            params["is_active"] = "true" if is_active else "false"
        if is_premium is not None:
            params["is_premium"] = "true" if is_premium else "false"

        # Realiza a chamada ao MS-Auth
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/api/auth/admin/users",
                params=params
            )

            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(
                    f"Erro ao obter usuários do MS-Auth: {response.status_code}")
                return {
                    "items": [],
                    "total": 0,
                    "page": 1,
                    "size": limit
                }
    except Exception as e:
        logger.error(f"Erro na comunicação com MS-Auth: {str(e)}")
        return {
            "items": [],
            "total": 0,
            "page": 1,
            "size": limit
        }


async def get_user_details(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Obtém detalhes completos de um usuário

    Args:
        user_id: ID do usuário

    Returns:
        Dados do usuário ou None se não encontrado
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/api/auth/admin/users/{user_id}"
            )

            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(
                    f"Erro ao obter detalhes do usuário {user_id}: {response.status_code}")
                return None
    except Exception as e:
        logger.error(
            f"Erro na comunicação com MS-Auth para usuário {user_id}: {str(e)}")
        return None


async def block_user(user_id: str, blocked: bool) -> bool:
    """
    Bloqueia ou desbloqueia um usuário

    Args:
        user_id: ID do usuário
        blocked: True para bloquear, False para desbloquear

    Returns:
        True se a operação foi bem-sucedida
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.patch(
                f"{AUTH_SERVICE_URL}/api/auth/admin/users/{user_id}/block",
                json={"blocked": blocked}
            )

            return response.status_code == 200
    except Exception as e:
        logger.error(
            f"Erro ao {('bloquear' if blocked else 'desbloquear')} usuário {user_id}: {str(e)}")
        return False


async def add_user_note(user_id: str, note: str, author_id: str) -> bool:
    """
    Adiciona uma nota administrativa a um usuário

    Args:
        user_id: ID do usuário
        note: Texto da nota
        author_id: ID do administrador que está adicionando a nota

    Returns:
        True se a operação foi bem-sucedida
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/api/auth/admin/users/{user_id}/notes",
                json={
                    "text": note,
                    "author_id": author_id
                }
            )

            return response.status_code == 201
    except Exception as e:
        logger.error(f"Erro ao adicionar nota ao usuário {user_id}: {str(e)}")
        return False


async def get_user_activity(user_id: str) -> Dict[str, Any]:
    """
    Obtém dados de atividade de um usuário específico

    Args:
        user_id: ID do usuário

    Returns:
        Dados de atividade do usuário
    """
    # Constrói os dados de atividade consultando diferentes microsserviços
    try:
        # Coleta dados de forma paralela
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Dados de login
            login_task = client.get(
                f"{AUTH_SERVICE_URL}/api/auth/admin/users/{user_id}/activity")
            # Dados de estudo
            study_task = client.get(
                f"{STUDY_SERVICE_URL}/api/study/admin/user/{user_id}/activity")
            # Dados de chat
            chat_task = client.get(
                f"{CHAT_SERVICE_URL}/api/chat/admin/user/{user_id}/activity")

            # Executa as chamadas
            login_response = await login_task
            study_response = await study_task
            chat_response = await chat_task

            # Processa as respostas
            login_data = login_response.json() if login_response.status_code == 200 else {}
            study_data = study_response.json() if study_response.status_code == 200 else {}
            chat_data = chat_response.json() if chat_response.status_code == 200 else {}

            # Combina os dados
            return {
                "login_activity": login_data,
                "study_activity": study_data,
                "chat_activity": chat_data,
                "last_seen": login_data.get("last_login_at")
            }
    except Exception as e:
        logger.error(f"Erro ao obter atividade do usuário {user_id}: {str(e)}")
        return {
            "login_activity": {},
            "study_activity": {},
            "chat_activity": {}
        }
