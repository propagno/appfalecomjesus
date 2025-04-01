from typing import Optional
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.api.deps import get_current_active_user, get_current_user
from app.schemas.progress import ReflectionCreate, ReflectionUpdate, ReflectionInDB, ReflectionDetail, ReflectionListResponse
from app.services.reflection_service import ReflectionService

router = APIRouter()


@router.get("/", response_model=ReflectionListResponse)
async def get_user_reflections(
    skip: int = Query(0, ge=0, description="Quantos itens pular"),
    limit: int = Query(
        10, ge=1, le=100, description="Limite de itens por página"),
    section_id: Optional[str] = Query(
        None, description="Filtrar por seção específica"),
    plan_id: Optional[str] = Query(
        None, description="Filtrar por plano específico"),
    sort_by: str = Query("created_at", description="Campo para ordenação"),
    sort_desc: bool = Query(True, description="Ordem decrescente"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna uma lista paginada das reflexões pessoais do usuário.

    Permite filtrar por seção ou plano específico.
    """
    reflection_service = ReflectionService(db)

    # Obter as reflexões do usuário
    reflections, total = await reflection_service.get_user_reflections(
        user_id=current_user["id"],
        skip=skip,
        limit=limit,
        section_id=section_id,
        plan_id=plan_id,
        sort_by=sort_by,
        sort_desc=sort_desc
    )

    # Calcular a página atual
    page = skip // limit + 1 if limit > 0 else 1

    return ReflectionListResponse(
        items=reflections,
        total=total,
        page=page,
        page_size=limit
    )


@router.post("/", response_model=ReflectionDetail, status_code=status.HTTP_201_CREATED)
async def create_reflection(
    reflection_data: ReflectionCreate,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Cria uma nova reflexão pessoal associada a uma seção de estudo.

    Requer autenticação.
    """
    reflection_service = ReflectionService(db)

    # Garantir que o user_id seja o do usuário autenticado
    if reflection_data.user_id != current_user["id"] and current_user["role"] != "admin":
        reflection_data.user_id = current_user["id"]

    # Criar a reflexão
    reflection = await reflection_service.create_reflection(reflection_data)

    return reflection


@router.get("/{reflection_id}", response_model=ReflectionDetail)
async def get_reflection(
    reflection_id: str = Path(..., description="ID da reflexão"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna uma reflexão específica pelo ID.

    Requer autenticação. Apenas o próprio usuário pode acessar suas reflexões.
    """
    reflection_service = ReflectionService(db)

    # Buscar a reflexão
    reflection = await reflection_service.get_reflection_detail(reflection_id)

    if not reflection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reflexão não encontrada"
        )

    # Verificar permissões (apenas o próprio usuário ou admin)
    if reflection.user_id != current_user["id"] and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não autorizado a acessar esta reflexão"
        )

    return reflection


@router.put("/{reflection_id}", response_model=ReflectionDetail)
async def update_reflection(
    reflection_update: ReflectionUpdate,
    reflection_id: str = Path(..., description="ID da reflexão"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza o texto de uma reflexão existente.

    Requer autenticação. Apenas o próprio usuário pode atualizar suas reflexões.
    """
    reflection_service = ReflectionService(db)

    # Buscar a reflexão existente
    existing_reflection = await reflection_service.get_reflection_by_id(reflection_id)

    if not existing_reflection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reflexão não encontrada"
        )

    # Verificar permissões (apenas o próprio usuário ou admin)
    if existing_reflection.user_id != current_user["id"] and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não autorizado a atualizar esta reflexão"
        )

    # Atualizar a reflexão
    updated_reflection = await reflection_service.update_reflection(reflection_id, reflection_update)

    return updated_reflection


@router.delete("/{reflection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reflection(
    reflection_id: str = Path(..., description="ID da reflexão"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Exclui uma reflexão existente.

    Requer autenticação. Apenas o próprio usuário pode excluir suas reflexões.
    """
    reflection_service = ReflectionService(db)

    # Buscar a reflexão existente
    existing_reflection = await reflection_service.get_reflection_by_id(reflection_id)

    if not existing_reflection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reflexão não encontrada"
        )

    # Verificar permissões (apenas o próprio usuário ou admin)
    if existing_reflection.user_id != current_user["id"] and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não autorizado a excluir esta reflexão"
        )

    # Excluir a reflexão
    await reflection_service.delete_reflection(reflection_id)

    return None


@router.get("/section/{section_id}", response_model=Optional[ReflectionDetail])
async def get_reflection_by_section(
    section_id: str = Path(..., description="ID da seção"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna a reflexão do usuário para uma seção específica.

    Útil para verificar se o usuário já fez uma reflexão sobre esta seção.
    """
    reflection_service = ReflectionService(db)

    # Buscar a reflexão para esta seção e usuário
    reflection = await reflection_service.get_reflection_by_section(
        user_id=current_user["id"],
        section_id=section_id
    )

    return reflection  # Pode ser None se não existir reflexão


@router.get("/recent", response_model=list[ReflectionDetail])
async def get_recent_reflections(
    limit: int = Query(
        5, ge=1, le=10, description="Número de reflexões recentes"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna as reflexões mais recentes do usuário.

    Útil para exibir as últimas reflexões na tela inicial.
    """
    reflection_service = ReflectionService(db)

    # Buscar as reflexões mais recentes do usuário
    recent_reflections = await reflection_service.get_recent_reflections(
        user_id=current_user["id"],
        limit=limit
    )

    return recent_reflections
