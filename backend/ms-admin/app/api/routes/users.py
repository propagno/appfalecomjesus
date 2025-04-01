from fastapi import APIRouter, Depends, Query, HTTPException, Body, Path
from typing import Optional, Any, Dict
from ...services import user_service
from ...api.deps import get_current_admin_user
from ...schemas.auth import User

router = APIRouter()


@router.get("/")
async def get_users(
    skip: int = Query(
        0, description="Número de registros para pular (paginação)"),
    limit: int = Query(
        20, description="Número máximo de registros a retornar"),
    search: Optional[str] = Query(
        None, description="Filtro por nome ou email"),
    is_active: Optional[bool] = Query(
        None, description="Filtrar por usuários ativos"),
    is_premium: Optional[bool] = Query(
        None, description="Filtrar por usuários premium"),
    sort_by: str = Query("created_at", description="Campo para ordenação"),
    sort_desc: bool = Query(True, description="Ordenar de forma descendente"),
    current_user: User = Depends(get_current_admin_user)
) -> Dict[str, Any]:
    """
    Obtém lista de usuários do sistema com filtros e paginação.

    Retorna um objeto com:
    - items: Lista de usuários
    - total: Número total de usuários que correspondem aos filtros
    - page: Número da página atual
    - size: Tamanho da página
    """
    return await user_service.get_users(
        skip=skip,
        limit=limit,
        search=search,
        is_active=is_active,
        is_premium=is_premium,
        sort_by=sort_by,
        sort_desc=sort_desc
    )


@router.get("/{user_id}")
async def get_user_details(
    user_id: str = Path(..., description="ID do usuário"),
    current_user: User = Depends(get_current_admin_user)
) -> Dict[str, Any]:
    """
    Obtém detalhes completos de um usuário específico, incluindo:
    - Informações básicas
    - Preferências
    - Status da assinatura
    - Histórico de atividades
    """
    user_data = await user_service.get_user_details(user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user_data


@router.patch("/{user_id}/block")
async def toggle_user_block(
    user_id: str = Path(..., description="ID do usuário"),
    is_blocked: bool = Body(..., embed=True, description="Status de bloqueio"),
    current_user: User = Depends(get_current_admin_user)
) -> Dict[str, bool]:
    """
    Bloqueia ou desbloqueia um usuário.

    Este endpoint pode ser usado para restringir o acesso de usuários problemáticos
    ou remover restrições previamente aplicadas.
    """
    success = await user_service.block_user(user_id, is_blocked)
    if not success:
        raise HTTPException(
            status_code=400, detail="Falha ao atualizar o status de bloqueio do usuário")

    return {"success": True}


@router.post("/{user_id}/notes")
async def add_user_note(
    user_id: str = Path(..., description="ID do usuário"),
    note: str = Body(..., embed=True,
                     description="Texto da nota administrativa"),
    current_user: User = Depends(get_current_admin_user)
) -> Dict[str, bool]:
    """
    Adiciona uma nota administrativa ao usuário.

    Estas notas são visíveis apenas para administradores e podem ser
    usadas para documentar ações específicas relacionadas ao usuário.
    """
    success = await user_service.add_user_note(user_id, note, current_user.id)
    if not success:
        raise HTTPException(
            status_code=400, detail="Falha ao adicionar nota ao usuário")

    return {"success": True}
