from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db, get_current_user
from app.schemas.study import (
    StudyPlanCreate,
    StudyPlanResponse,
    StudySectionCreate,
    StudySectionResponse,
    StudyContentCreate,
    StudyContentResponse,
    UserStudyProgressCreate,
    UserStudyProgressResponse
)
from app.services.study import StudyService

router = APIRouter()


@router.post("/plans", response_model=StudyPlanResponse)
async def create_study_plan(
    plan: StudyPlanCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Cria um novo plano de estudo para o usuário.
    """
    return await StudyService.create_study_plan(db, current_user.id, plan)


@router.get("/plans", response_model=List[StudyPlanResponse])
async def get_user_study_plans(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Lista todos os planos de estudo do usuário.
    """
    return await StudyService.get_user_study_plans(db, current_user.id)


@router.get("/plans/{plan_id}", response_model=StudyPlanResponse)
async def get_study_plan(
    plan_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Obtém detalhes de um plano de estudo específico.
    """
    plan = await StudyService.get_study_plan(db, plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano de estudo não encontrado"
        )
    return plan


@router.post("/plans/{plan_id}/sections", response_model=StudySectionResponse)
async def create_study_section(
    plan_id: str,
    section: StudySectionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Cria uma nova seção em um plano de estudo.
    """
    plan = await StudyService.get_study_plan(db, plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano de estudo não encontrado"
        )
    return await StudyService.create_study_section(db, plan_id, section)


@router.post("/sections/{section_id}/content", response_model=StudyContentResponse)
async def create_study_content(
    section_id: str,
    content: StudyContentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Adiciona conteúdo a uma seção de estudo.
    """
    return await StudyService.create_study_content(db, section_id, content)


@router.get("/current", response_model=dict)
async def get_current_study(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Obtém o estudo atual do usuário.
    """
    study = await StudyService.get_current_study(db, current_user.id)
    if not study:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum estudo em andamento"
        )
    return study


@router.post("/progress", response_model=UserStudyProgressResponse)
async def update_study_progress(
    progress: UserStudyProgressCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Atualiza o progresso do usuário no estudo.
    """
    return await StudyService.update_study_progress(db, current_user.id, progress)


@router.get("/progress/{plan_id}", response_model=UserStudyProgressResponse)
async def get_study_progress(
    plan_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Obtém o progresso do usuário em um plano específico.
    """
    progress = await StudyService.get_study_progress(db, current_user.id, plan_id)
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progresso não encontrado"
        )
    return progress
