from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.api.deps import get_current_active_user, get_current_user
from app.schemas.study_plan import (
    StudyPlanCreate,
    StudyPlanUpdate,
    StudyPlanInDB,
    StudyPlanSimple,
    StudyPlanListResponse
)
from app.services.study_plan_service import StudyPlanService

router = APIRouter()


@router.get("/", response_model=StudyPlanListResponse)
async def get_study_plans(
    skip: int = Query(0, ge=0, description="Quantos itens pular"),
    limit: int = Query(
        10, ge=1, le=100, description="Limite de itens por página"),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    difficulty: Optional[str] = Query(
        None, description="Filtrar por dificuldade"),
    search: Optional[str] = Query(
        None, description="Buscar por título ou descrição"),
    public_only: bool = Query(
        False, description="Mostrar apenas planos públicos"),
    sort_by: str = Query("created_at", description="Campo para ordenação"),
    sort_desc: bool = Query(True, description="Ordem decrescente"),
    current_user: Optional[dict] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna uma lista paginada de planos de estudo disponíveis.

    Se autenticado, inclui planos personalizados do usuário atual.
    Se não autenticado ou public_only=True, retorna apenas planos públicos.
    """
    study_plan_service = StudyPlanService(db)

    # Obter o ID do usuário se estiver autenticado
    user_id = current_user.get("id") if current_user else None

    # Obter os planos de estudo
    plans, total = await study_plan_service.get_plans(
        skip=skip,
        limit=limit,
        category=category,
        difficulty=difficulty,
        search=search,
        user_id=user_id,
        # Se não autenticado, mostra apenas públicos
        public_only=public_only if user_id else True,
        sort_by=sort_by,
        sort_desc=sort_desc
    )

    # Calcular a página atual
    page = skip // limit + 1 if limit > 0 else 1

    return StudyPlanListResponse(
        items=plans,
        total=total,
        page=page,
        page_size=limit
    )


@router.post("/", response_model=StudyPlanInDB, status_code=status.HTTP_201_CREATED)
async def create_study_plan(
    study_plan: StudyPlanCreate,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Cria um novo plano de estudo associado ao usuário atual.

    Requer autenticação. Opcionalmente pode criar um plano público.
    """
    study_plan_service = StudyPlanService(db)

    # Garantir que o user_id do plano seja o do usuário autenticado
    if study_plan.user_id and study_plan.user_id != current_user["id"]:
        if current_user["role"] != "admin":
            study_plan.user_id = current_user["id"]
    else:
        study_plan.user_id = current_user["id"]

    return await study_plan_service.create_plan(study_plan)


@router.get("/{plan_id}", response_model=StudyPlanInDB)
async def get_study_plan(
    plan_id: str = Path(..., description="ID do plano de estudo"),
    current_user: Optional[dict] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna um plano de estudo específico pelo ID.

    Se o plano for privado, apenas o dono ou admin pode acessá-lo.
    """
    study_plan_service = StudyPlanService(db)
    study_plan = await study_plan_service.get_plan_by_id(plan_id)

    if not study_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano de estudo não encontrado"
        )

    # Verificar se o usuário tem permissão para acessar o plano
    if not study_plan.is_public:
        if not current_user or (study_plan.user_id != current_user.get("id") and current_user.get("role") != "admin"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso não autorizado a este plano"
            )

    return study_plan


@router.put("/{plan_id}", response_model=StudyPlanInDB)
async def update_study_plan(
    plan_update: StudyPlanUpdate,
    plan_id: str = Path(..., description="ID do plano de estudo"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza um plano de estudo existente.

    Apenas o dono do plano ou um admin pode atualizá-lo.
    """
    study_plan_service = StudyPlanService(db)

    # Verificar se o plano existe
    existing_plan = await study_plan_service.get_plan_by_id(plan_id)
    if not existing_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano de estudo não encontrado"
        )

    # Verificar permissões
    if existing_plan.user_id != current_user["id"] and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não autorizado a editar este plano"
        )

    # Atualizar o plano
    return await study_plan_service.update_plan(plan_id, plan_update)


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_study_plan(
    plan_id: str = Path(..., description="ID do plano de estudo"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Exclui um plano de estudo existente.

    Apenas o dono do plano ou um admin pode excluí-lo.
    """
    study_plan_service = StudyPlanService(db)

    # Verificar se o plano existe
    existing_plan = await study_plan_service.get_plan_by_id(plan_id)
    if not existing_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano de estudo não encontrado"
        )

    # Verificar permissões
    if existing_plan.user_id != current_user["id"] and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não autorizado a excluir este plano"
        )

    # Excluir o plano
    await study_plan_service.delete_plan(plan_id)

    return None


@router.get("/category/{category}", response_model=List[StudyPlanSimple])
async def get_plans_by_category(
    category: str = Path(..., description="Categoria do plano"),
    limit: int = Query(
        5, ge=1, le=20, description="Limite de planos a retornar"),
    current_user: Optional[dict] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna planos de estudo por categoria.

    Útil para recomendações na interface.
    """
    study_plan_service = StudyPlanService(db)

    # Obter o ID do usuário se estiver autenticado
    user_id = current_user.get("id") if current_user else None

    plans, _ = await study_plan_service.get_plans(
        limit=limit,
        category=category,
        user_id=user_id,
        # Se não autenticado, mostra apenas públicos
        public_only=not bool(user_id),
        sort_by="created_at",
        sort_desc=True
    )

    return plans


@router.get("/recommendations", response_model=List[StudyPlanSimple])
async def get_plan_recommendations(
    limit: int = Query(5, ge=1, le=10, description="Número de recomendações"),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna recomendações de planos de estudo para o usuário.

    Baseado em histórico e preferências.
    """
    study_plan_service = StudyPlanService(db)

    # Obter recomendações personalizadas
    # Esta é uma implementação simplificada - em um sistema real, usaria algoritmos mais avançados
    recommendations = await study_plan_service.get_recommendations(
        user_id=current_user["id"],
        limit=limit
    )

    return recommendations
