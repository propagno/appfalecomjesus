from typing import Optional
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.api.deps import get_current_active_user, get_current_user
from app.schemas.progress import (
    UserStudyProgressCreate,
    UserStudyProgressUpdate,
    UserStudyProgressInDB,
    UserStudyProgressDetail,
    UserStudyProgressListResponse
)
from app.services.progress_service import ProgressService

router = APIRouter()


@router.get("/", response_model=UserStudyProgressListResponse)
async def get_user_progress_list(
    skip: int = Query(0, ge=0, description="Quantos itens pular"),
    limit: int = Query(
        10, ge=1, le=100, description="Limite de itens por página"),
    completed: Optional[bool] = Query(
        None, description="Filtrar por status de conclusão"),
    sort_by: str = Query("last_activity_date",
                         description="Campo para ordenação"),
    sort_desc: bool = Query(True, description="Ordem decrescente"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna uma lista paginada do progresso do usuário em seus planos de estudo.

    Permite filtrar por status de conclusão e ordenar por diferentes campos.
    """
    progress_service = ProgressService(db)

    # Obter o progresso do usuário
    progress_list, total = await progress_service.get_user_progress_list(
        user_id=current_user["id"],
        skip=skip,
        limit=limit,
        completed=completed,
        sort_by=sort_by,
        sort_desc=sort_desc
    )

    # Calcular a página atual
    page = skip // limit + 1 if limit > 0 else 1

    return UserStudyProgressListResponse(
        items=progress_list,
        total=total,
        page=page,
        page_size=limit
    )


@router.post("/", response_model=UserStudyProgressInDB, status_code=status.HTTP_201_CREATED)
async def start_study_plan(
    progress_data: UserStudyProgressCreate,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Inicia um novo plano de estudo para o usuário atual.

    Se o usuário já tiver iniciado o plano, retorna o progresso existente.
    """
    progress_service = ProgressService(db)

    # Garantir que o user_id seja o do usuário autenticado
    if progress_data.user_id != current_user["id"] and current_user["role"] != "admin":
        progress_data.user_id = current_user["id"]

    return await progress_service.start_study_plan(progress_data)


@router.get("/{progress_id}", response_model=UserStudyProgressDetail)
async def get_progress_detail(
    progress_id: str = Path(..., description="ID do progresso"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna detalhes do progresso específico de um usuário em um plano de estudo.

    Inclui informações sobre o plano e a seção atual.
    """
    progress_service = ProgressService(db)

    # Buscar o progresso
    progress = await progress_service.get_progress_detail(progress_id)

    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progresso não encontrado"
        )

    # Verificar permissões (apenas o próprio usuário ou admin)
    if progress.user_id != current_user["id"] and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não autorizado a acessar este progresso"
        )

    return progress


@router.put("/{progress_id}", response_model=UserStudyProgressDetail)
async def update_progress(
    progress_update: UserStudyProgressUpdate,
    progress_id: str = Path(..., description="ID do progresso"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza o progresso do usuário em um plano de estudo.

    Permite avançar para a próxima seção, marcar porcentagem de conclusão, etc.
    """
    progress_service = ProgressService(db)

    # Buscar o progresso existente
    existing_progress = await progress_service.get_progress_by_id(progress_id)

    if not existing_progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progresso não encontrado"
        )

    # Verificar permissões (apenas o próprio usuário ou admin)
    if existing_progress.user_id != current_user["id"] and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não autorizado a atualizar este progresso"
        )

    # Atualizar o progresso
    updated_progress = await progress_service.update_progress(progress_id, progress_update)

    return updated_progress


@router.get("/plan/{plan_id}", response_model=UserStudyProgressDetail)
async def get_progress_by_plan(
    plan_id: str = Path(..., description="ID do plano de estudo"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna o progresso do usuário atual em um plano de estudo específico.

    Se o usuário não tiver iniciado o plano, retorna 404.
    """
    progress_service = ProgressService(db)

    # Buscar o progresso do usuário neste plano
    progress = await progress_service.get_progress_by_plan(
        user_id=current_user["id"],
        plan_id=plan_id
    )

    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progresso não encontrado para este plano"
        )

    return progress


@router.post("/plan/{plan_id}/complete-section", response_model=UserStudyProgressDetail)
async def complete_current_section(
    plan_id: str = Path(..., description="ID do plano de estudo"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Marca a seção atual como concluída e avança para a próxima seção do plano.

    Se for a última seção, marca o plano como concluído.
    """
    progress_service = ProgressService(db)

    # Atualizar o progresso para a próxima seção
    try:
        updated_progress = await progress_service.complete_section(
            user_id=current_user["id"],
            plan_id=plan_id
        )
        return updated_progress
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{progress_id}", status_code=status.HTTP_204_NO_CONTENT)
async def reset_progress(
    progress_id: str = Path(..., description="ID do progresso"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Reseta o progresso do usuário em um plano de estudo, ou exclui se especificado.

    Por padrão, apenas reseta o progresso para 0%, mas mantém o registro.
    """
    progress_service = ProgressService(db)

    # Buscar o progresso existente
    existing_progress = await progress_service.get_progress_by_id(progress_id)

    if not existing_progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progresso não encontrado"
        )

    # Verificar permissões (apenas o próprio usuário ou admin)
    if existing_progress.user_id != current_user["id"] and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não autorizado a resetar este progresso"
        )

    # Resetar o progresso
    await progress_service.reset_progress(progress_id)

    return None


@router.get("/active", response_model=UserStudyProgressDetail)
async def get_active_study(
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna o plano de estudo ativo mais recente do usuário.

    Útil para mostrar a opção "Continuar estudando" na interface.
    """
    progress_service = ProgressService(db)

    # Buscar o progresso mais recente não concluído
    active_progress = await progress_service.get_active_study(user_id=current_user["id"])

    if not active_progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum estudo ativo encontrado"
        )

    return active_progress
