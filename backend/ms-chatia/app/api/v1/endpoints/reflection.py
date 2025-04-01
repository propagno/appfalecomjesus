from typing import Dict, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.logging import get_logger
from app.schemas.reflection import (
    Reflection,
    ReflectionCreate,
    ReflectionUpdate
)
from app.services.reflection_service import ReflectionService

router = APIRouter()
logger = get_logger(__name__)


@router.post(
    "/reflections",
    response_model=Reflection,
    status_code=status.HTTP_201_CREATED,
    summary="Criar reflexão",
    description="""
    Salva uma nova reflexão pessoal do usuário.
    
    A reflexão pode estar vinculada a:
    - Uma seção de estudo específica
    - Um versículo específico
    - Uma mensagem do chat IA
    
    O texto é armazenado de forma segura e privada.
    """
)
async def create_reflection(
    *,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user),
    reflection: ReflectionCreate
) -> Reflection:
    """
    Cria uma nova reflexão pessoal.

    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        reflection: Dados da reflexão

    Returns:
        Reflection com detalhes salvos

    Raises:
        HTTPException: Se erro na criação
    """
    try:
        reflection_service = ReflectionService(db)
        return await reflection_service.create_reflection(
            user_id=current_user["id"],
            reflection=reflection
        )
    except Exception as e:
        logger.error(f"Error creating reflection: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao salvar reflexão"
        )


@router.get(
    "/reflections/{reflection_id}",
    response_model=Reflection,
    summary="Buscar reflexão",
    description="""
    Recupera uma reflexão específica do usuário.
    
    Inclui:
    - Texto da reflexão
    - Data de criação
    - Referências (estudo, versículo ou chat)
    - Tags e categorias
    """
)
async def get_reflection(
    reflection_id: UUID,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> Reflection:
    """
    Recupera uma reflexão específica.

    Args:
        reflection_id: ID da reflexão
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Reflection com detalhes

    Raises:
        HTTPException: Se reflexão não encontrada ou acesso negado
    """
    try:
        reflection_service = ReflectionService(db)
        return await reflection_service.get_reflection(
            user_id=current_user["id"],
            reflection_id=reflection_id
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting reflection: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao recuperar reflexão"
        )


@router.get(
    "/reflections",
    response_model=List[Reflection],
    summary="Listar reflexões",
    description="""
    Lista todas as reflexões do usuário.
    
    Permite filtrar por:
    - Data
    - Plano de estudo
    - Versículo
    - Tags
    
    Ordenado por data mais recente.
    """
)
async def list_reflections(
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user),
    study_plan_id: UUID = None,
    verse_id: UUID = None,
    tag: str = None
) -> List[Reflection]:
    """
    Lista todas as reflexões do usuário.

    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        study_plan_id: Filtro por plano (opcional)
        verse_id: Filtro por versículo (opcional)
        tag: Filtro por tag (opcional)

    Returns:
        Lista de Reflection

    Raises:
        HTTPException: Se erro na listagem
    """
    try:
        reflection_service = ReflectionService(db)
        return await reflection_service.list_reflections(
            user_id=current_user["id"],
            study_plan_id=study_plan_id,
            verse_id=verse_id,
            tag=tag
        )
    except Exception as e:
        logger.error(f"Error listing reflections: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar reflexões"
        )


@router.put(
    "/reflections/{reflection_id}",
    response_model=Reflection,
    summary="Atualizar reflexão",
    description="""
    Atualiza uma reflexão existente.
    
    Permite alterar:
    - Texto
    - Tags
    - Referências
    
    Mantém data original de criação.
    """
)
async def update_reflection(
    *,
    reflection_id: UUID,
    reflection: ReflectionUpdate,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> Reflection:
    """
    Atualiza uma reflexão existente.

    Args:
        reflection_id: ID da reflexão
        reflection: Dados a atualizar
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Reflection atualizada

    Raises:
        HTTPException: Se reflexão não encontrada ou erro na atualização
    """
    try:
        reflection_service = ReflectionService(db)
        return await reflection_service.update_reflection(
            user_id=current_user["id"],
            reflection_id=reflection_id,
            reflection_data=reflection
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating reflection: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar reflexão"
        )


@router.delete(
    "/reflections/{reflection_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir reflexão",
    description="""
    Remove uma reflexão existente.
    
    A exclusão é permanente e não pode ser desfeita.
    Apenas o próprio usuário pode excluir suas reflexões.
    """
)
async def delete_reflection(
    reflection_id: UUID,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Remove uma reflexão existente.

    Args:
        reflection_id: ID da reflexão
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Raises:
        HTTPException: Se reflexão não encontrada ou erro na exclusão
    """
    try:
        reflection_service = ReflectionService(db)
        await reflection_service.delete_reflection(
            user_id=current_user["id"],
            reflection_id=reflection_id
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting reflection: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao excluir reflexão"
        )
