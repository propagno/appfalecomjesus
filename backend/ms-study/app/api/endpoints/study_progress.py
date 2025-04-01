import uuid
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks

from app.schemas.study_progress import (
    UserStudyProgressCreate,
    UserStudyProgressUpdate,
    UserStudyProgressRead,
    UserStudyProgressList
)
from app.services.study_progress_service import StudyProgressService
from app.services.certificate_service import CertificateService
from app.api.deps import get_current_user, get_study_progress_service, get_certificate_service


router = APIRouter()


@router.post(
    "/",
    response_model=UserStudyProgressRead,
    status_code=status.HTTP_201_CREATED,
    summary="Iniciar ou atualizar progresso em um plano de estudo"
)
async def create_or_update_progress(
    request: UserStudyProgressUpdate,
    background_tasks: BackgroundTasks,
    current_user=Depends(get_current_user),
    progress_service: StudyProgressService = Depends(
        get_study_progress_service),
    certificate_service: CertificateService = Depends(get_certificate_service)
) -> Any:
    """
    Cria ou atualiza o progresso de um usuário em um plano de estudo.

    Se o plano de estudo atingir 100% de conclusão, um certificado será gerado automaticamente.
    """
    # Converter os IDs de string para UUID
    user_id = uuid.UUID(str(current_user.id))
    study_plan_id = uuid.UUID(str(request.study_plan_id))

    # Atualizar progresso
    section_id = uuid.UUID(str(request.current_section_id)
                           ) if request.current_section_id else None
    progress, plan_completed = await progress_service.update_progress(
        user_id=user_id,
        study_plan_id=study_plan_id,
        section_id=section_id,
        completion_percentage=request.completion_percentage
    )

    # Se o plano foi concluído agora, gerar certificado em background
    if plan_completed:
        background_tasks.add_task(
            certificate_service.generate_certificate,
            user_id=user_id,
            study_plan_id=study_plan_id
        )

    # Converter para o schema de retorno
    return UserStudyProgressRead(
        id=str(progress.id),
        user_id=str(progress.user_id),
        study_plan_id=str(progress.study_plan_id),
        current_section_id=str(
            progress.current_section_id) if progress.current_section_id else None,
        completion_percentage=progress.completion_percentage,
        created_at=progress.created_at,
        updated_at=progress.updated_at
    )


@router.get(
    "/",
    response_model=UserStudyProgressList,
    status_code=status.HTTP_200_OK,
    summary="Listar progresso em todos os planos de estudo"
)
async def list_all_progress(
    current_user=Depends(get_current_user),
    progress_service: StudyProgressService = Depends(
        get_study_progress_service)
) -> Any:
    """
    Lista o progresso do usuário em todos os planos de estudo.
    """
    user_id = uuid.UUID(str(current_user.id))
    progress_list = await progress_service.get_all_user_progress(user_id)

    # Converter para o schema de retorno
    items = []
    for item in progress_list:
        progress = item["progress"]
        plan = item["plan"]

        items.append({
            "id": str(progress.id),
            "user_id": str(progress.user_id),
            "study_plan_id": str(progress.study_plan_id),
            "study_plan_title": plan.title,
            "current_section_id": str(progress.current_section_id) if progress.current_section_id else None,
            "completion_percentage": progress.completion_percentage,
            "created_at": progress.created_at,
            "updated_at": progress.updated_at
        })

    return UserStudyProgressList(items=items)


@router.get(
    "/{study_plan_id}",
    response_model=UserStudyProgressRead,
    status_code=status.HTTP_200_OK,
    summary="Obter progresso em um plano de estudo específico"
)
async def get_plan_progress(
    study_plan_id: uuid.UUID,
    current_user=Depends(get_current_user),
    progress_service: StudyProgressService = Depends(
        get_study_progress_service)
) -> Any:
    """
    Obtém o progresso do usuário em um plano de estudo específico.
    """
    user_id = uuid.UUID(str(current_user.id))
    progress = await progress_service.get_user_progress(user_id, study_plan_id)

    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progresso não encontrado para este plano de estudo"
        )

    # Converter para o schema de retorno
    return UserStudyProgressRead(
        id=str(progress.id),
        user_id=str(progress.user_id),
        study_plan_id=str(progress.study_plan_id),
        current_section_id=str(
            progress.current_section_id) if progress.current_section_id else None,
        completion_percentage=progress.completion_percentage,
        created_at=progress.created_at,
        updated_at=progress.updated_at
    )


@router.post(
    "/start-plan",
    response_model=UserStudyProgressRead,
    status_code=status.HTTP_201_CREATED,
    summary="Iniciar um plano de estudo"
)
async def start_study_plan(
    request: UserStudyProgressCreate,
    current_user=Depends(get_current_user),
    progress_service: StudyProgressService = Depends(
        get_study_progress_service)
) -> Any:
    """
    Inicia um plano de estudo para o usuário.
    """
    user_id = uuid.UUID(str(current_user.id))
    study_plan_id = uuid.UUID(str(request.study_plan_id))
    first_section_id = uuid.UUID(
        str(request.first_section_id)) if request.first_section_id else None

    progress = await progress_service.start_plan(
        user_id=user_id,
        study_plan_id=study_plan_id,
        first_section_id=first_section_id
    )

    # Converter para o schema de retorno
    return UserStudyProgressRead(
        id=str(progress.id),
        user_id=str(progress.user_id),
        study_plan_id=str(progress.study_plan_id),
        current_section_id=str(
            progress.current_section_id) if progress.current_section_id else None,
        completion_percentage=progress.completion_percentage,
        created_at=progress.created_at,
        updated_at=progress.updated_at
    )


@router.get(
    "/completed",
    response_model=UserStudyProgressList,
    status_code=status.HTTP_200_OK,
    summary="Listar planos de estudo concluídos"
)
async def list_completed_plans(
    current_user=Depends(get_current_user),
    progress_service: StudyProgressService = Depends(
        get_study_progress_service)
) -> Any:
    """
    Lista todos os planos de estudo concluídos pelo usuário.
    """
    user_id = uuid.UUID(str(current_user.id))
    completed_plans = await progress_service.get_completed_plans(user_id)

    # Converter para o schema de retorno
    items = []
    for item in completed_plans:
        progress = item["progress"]
        plan = item["plan"]

        items.append({
            "id": str(progress.id),
            "user_id": str(progress.user_id),
            "study_plan_id": str(progress.study_plan_id),
            "study_plan_title": plan.title,
            "current_section_id": str(progress.current_section_id) if progress.current_section_id else None,
            "completion_percentage": progress.completion_percentage,
            "created_at": progress.created_at,
            "updated_at": progress.updated_at
        })

    return UserStudyProgressList(items=items)
