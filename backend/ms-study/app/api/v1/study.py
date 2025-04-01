from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
import logging
import httpx
from fastapi.concurrency import run_in_threadpool

from app.api.v1.dependencies import get_study_service, get_current_active_user, verify_service_api_key
from app.domain.study.schemas import (
    UserPreferences, UserPreferencesResponse, StudyPlanResponse, UserStudyProgressCreate,
    UserStudyProgressResponse, UserReflectionCreate, UserReflectionResponse,
    StudySectionResponse, StudyContentResponse, DailyDevotionalResponse
)
from app.domain.study.service import StudyService
from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger("study_router")

study_router = APIRouter()


@study_router.get("/health")
async def health_check():
    """
    Health check endpoint para MS-Study.
    """
    return {"status": "healthy", "service": "ms-study"}


async def get_user_details(user_id: str) -> Dict[str, str]:
    """
    Obtém os detalhes do usuário a partir do MS-Auth
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{settings.MS_AUTH_URL}/api/v1/auth/users/{user_id}",
                headers={"Authorization": f"Bearer {settings.SERVICE_API_KEY}"}
            )

            if response.status_code == 200:
                user_data = response.json()
                return {
                    "id": user_data.get("id", user_id),
                    "name": user_data.get("name", "Usuário"),
                    "email": user_data.get("email", "")
                }
            else:
                logger.warning(
                    f"Could not get user details from ms-auth: {response.status_code}")
                return {"id": user_id, "name": "Usuário", "email": ""}
    except Exception as e:
        logger.error(f"Error getting user details: {str(e)}")
        return {"id": user_id, "name": "Usuário", "email": ""}


@study_router.post("/plans", response_model=StudyPlanResponse)
async def create_study_plan(
    preferences: UserPreferences,
    current_user: dict = Depends(get_current_active_user),
    study_service: StudyService = Depends(get_study_service)
):
    """
    Create a new personalized study plan based on user preferences.
    """
    try:
        # Get user details from auth service if not provided
        if not preferences.name or not preferences.email:
            user_details = await get_user_details(current_user["id"])
            preferences.name = user_details["name"]
            preferences.email = user_details["email"]

        # Override the user_id from preferences with the authenticated user ID
        preferences.user_id = current_user["id"]

        plan = await study_service.generate_study_plan(preferences)
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao gerar plano de estudo"
            )
        return plan
    except Exception as e:
        logger.error(f"Error creating study plan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar plano de estudo: {str(e)}"
        )


@study_router.get("/plans", response_model=List[StudyPlanResponse])
async def get_user_study_plans(
    current_user: dict = Depends(get_current_active_user),
    study_service: StudyService = Depends(get_study_service)
):
    """
    Get all study plans for the current user.
    """
    try:
        return study_service.get_study_plans_by_user(current_user["id"])
    except Exception as e:
        logger.error(f"Error getting study plans: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter planos de estudo: {str(e)}"
        )


@study_router.get("/plans/{plan_id}", response_model=StudyPlanResponse)
async def get_study_plan(
    plan_id: str = Path(..., description="ID do plano de estudo"),
    current_user: dict = Depends(get_current_active_user),
    study_service: StudyService = Depends(get_study_service)
):
    """
    Get a specific study plan by ID.
    """
    plan = study_service.get_study_plan(plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano de estudo não encontrado"
        )

    # Check if the plan belongs to the current user
    if plan.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado a este plano de estudo"
        )

    return plan


@study_router.get("/plans/{plan_id}/sections", response_model=List[StudySectionResponse])
async def get_plan_sections(
    plan_id: str = Path(..., description="ID do plano de estudo"),
    current_user: dict = Depends(get_current_active_user),
    study_service: StudyService = Depends(get_study_service)
):
    """
    Get all sections for a specific study plan.
    """
    plan = study_service.get_study_plan(plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano de estudo não encontrado"
        )

    # Check if the plan belongs to the current user
    if plan.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado a este plano de estudo"
        )

    return study_service.get_sections_by_plan(plan_id)


@study_router.get("/sections/{section_id}", response_model=StudySectionResponse)
async def get_section(
    section_id: str = Path(..., description="ID da seção de estudo"),
    current_user: dict = Depends(get_current_active_user),
    study_service: StudyService = Depends(get_study_service)
):
    """
    Get a specific study section by ID.
    """
    section = study_service.get_section(section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seção de estudo não encontrada"
        )

    # Get the plan to check ownership
    plan = study_service.get_study_plan(section.study_plan_id)
    if plan.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado a esta seção de estudo"
        )

    return section


@study_router.get("/sections/{section_id}/contents", response_model=List[StudyContentResponse])
async def get_section_contents(
    section_id: str = Path(..., description="ID da seção de estudo"),
    current_user: dict = Depends(get_current_active_user),
    study_service: StudyService = Depends(get_study_service)
):
    """
    Get all contents for a specific study section.
    """
    section = study_service.get_section(section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seção de estudo não encontrada"
        )

    # Get the plan to check ownership
    plan = study_service.get_study_plan(section.study_plan_id)
    if plan.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado a esta seção de estudo"
        )

    return study_service.get_section_contents(section_id)


@study_router.post("/progress", response_model=UserStudyProgressResponse)
async def update_progress(
    progress_data: UserStudyProgressCreate,
    current_user: dict = Depends(get_current_active_user),
    study_service: StudyService = Depends(get_study_service)
):
    """
    Update the user's progress on a specific study section.
    """
    # Get the section to check if it exists
    section = study_service.get_section(progress_data.section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seção de estudo não encontrada"
        )

    # Get the plan to check ownership
    plan = study_service.get_study_plan(section.study_plan_id)
    if plan.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado a esta seção de estudo"
        )

    try:
        return study_service.update_user_progress(current_user["id"], progress_data)
    except Exception as e:
        logger.error(f"Error updating progress: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar progresso: {str(e)}"
        )


@study_router.post("/reflections", response_model=UserReflectionResponse)
async def save_reflection(
    reflection_data: UserReflectionCreate,
    current_user: dict = Depends(get_current_active_user),
    study_service: StudyService = Depends(get_study_service)
):
    """
    Save the user's reflection on a specific study section.
    """
    # Get the section to check if it exists
    section = study_service.get_section(reflection_data.section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seção de estudo não encontrada"
        )

    # Get the plan to check ownership
    plan = study_service.get_study_plan(section.study_plan_id)
    if plan.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado a esta seção de estudo"
        )

    try:
        return study_service.save_user_reflection(current_user["id"], reflection_data)
    except Exception as e:
        logger.error(f"Error saving reflection: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar reflexão: {str(e)}"
        )


@study_router.get("/plans/{plan_id}/progress", response_model=Dict[str, UserStudyProgressResponse])
async def get_plan_progress(
    plan_id: str = Path(..., description="ID do plano de estudo"),
    current_user: dict = Depends(get_current_active_user),
    study_service: StudyService = Depends(get_study_service)
):
    """
    Get the user's progress on all sections of a specific study plan.
    """
    plan = study_service.get_study_plan(plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano de estudo não encontrado"
        )

    # Check if the plan belongs to the current user
    if plan.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado a este plano de estudo"
        )

    return study_service.get_user_progress_by_plan(current_user["id"], plan_id)


@study_router.get("/daily-devotional", response_model=DailyDevotionalResponse)
async def get_daily_devotional(
    current_user: dict = Depends(get_current_active_user),
    study_service: StudyService = Depends(get_study_service)
):
    """
    Get a daily devotional content.
    """
    try:
        return study_service.get_random_devotional()
    except Exception as e:
        logger.error(f"Error getting daily devotional: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter devocional diário: {str(e)}"
        )

# Endpoint para receber preferências de estudo do ms-auth durante o onboarding


@study_router.post("/preferences", response_model=UserPreferencesResponse)
async def save_user_preferences(
    preferences: UserPreferences,
    current_user: dict = Depends(get_current_active_user),
    study_service: StudyService = Depends(get_study_service)
):
    """
    Save user preferences during the onboarding process.
    These preferences will be used to generate a personalized study plan.
    """
    try:
        # Override the user_id with the authenticated user's ID for security
        preferences.user_id = current_user["id"]

        # If name or email is not provided, get it from the user service
        if not preferences.name or not preferences.email:
            user_details = await get_user_details(current_user["id"])
            preferences.name = user_details["name"]
            preferences.email = user_details["email"]

        # Save the preferences
        db_preferences = study_service.create_or_update_user_preferences(
            preferences)

        # Return the saved preferences
        return db_preferences
    except Exception as e:
        logger.error(f"Error saving user preferences: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar preferências do usuário: {str(e)}"
        )


@study_router.get("/preferences", response_model=UserPreferencesResponse)
async def get_user_preferences(
    current_user: dict = Depends(get_current_active_user),
    study_service: StudyService = Depends(get_study_service)
):
    """
    Get current user preferences.
    """
    preferences = study_service.get_user_preferences(current_user["id"])
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferências do usuário não encontradas"
        )
    return preferences


@study_router.post("/onboarding/complete", response_model=UserPreferencesResponse)
async def complete_onboarding(
    current_user: dict = Depends(get_current_active_user),
    study_service: StudyService = Depends(get_study_service)
):
    """
    Mark the onboarding process as completed for the current user.
    """
    preferences = study_service.set_onboarding_completed(
        current_user["id"], True)
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferências do usuário não encontradas"
        )
    return preferences

# New endpoint for external service to initialize a study plan


@study_router.post("/init-plan", status_code=status.HTTP_201_CREATED, response_model=StudyPlanResponse)
async def initialize_study_plan(
    current_user: dict = Depends(get_current_active_user),
    study_service: StudyService = Depends(get_study_service)
):
    """
    Inicializa um plano de estudo personalizado para o usuário.
    Primeiro verifica se já existe um plano, caso contrário, cria um novo.
    """
    try:
        logger.info(
            f"Iniciando plano de estudo para usuário {current_user['id']}")

        # Verificar se já existe algum plano para o usuário
        existing_plans = study_service.get_study_plans_by_user(
            current_user["id"])
        if existing_plans and len(existing_plans) > 0:
            # Retorna o plano mais recente já existente
            most_recent_plan = max(existing_plans, key=lambda p: p.created_at)
            logger.info(
                f"Encontrado plano existente {most_recent_plan.id} para usuário {current_user['id']}")
            return most_recent_plan

        # Obter preferências do usuário
        user_preferences = study_service.get_user_preferences(
            current_user["id"])

        if not user_preferences:
            # Não foi possível encontrar preferências, cria plano com valores padrão
            logger.warning(
                f"Nenhuma preferência encontrada para usuário {current_user['id']}")

            # Valores padrão genéricos
            preferences = UserPreferences(
                user_id=current_user["id"],
                objectives=["crescimento espiritual", "conhecimento bíblico"],
                bible_experience_level="iniciante",
                content_preferences=["textos curtos", "reflexões"],
                preferred_time="qualquer"
            )
        else:
            # Criar objeto de preferências com os dados existentes
            preferences = UserPreferences(
                user_id=current_user["id"],
                objectives=user_preferences.objectives,
                bible_experience_level=user_preferences.bible_experience_level,
                content_preferences=user_preferences.content_preferences,
                preferred_time=user_preferences.preferred_time
            )

        # Adicionar detalhes do usuário se necessário
        user_details = await get_user_details(current_user["id"])
        preferences.name = user_details.get("name")
        preferences.email = user_details.get("email")

        # Gerar o plano personalizado
        logger.info(
            f"Gerando plano personalizado para usuário {current_user['id']}")
        plan = await study_service.generate_study_plan(preferences)

        if not plan:
            logger.error(
                f"Falha ao gerar plano para usuário {current_user['id']}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao gerar plano de estudo personalizado"
            )

        # Atualizar o status das preferências do usuário
        try:
            study_service.update_user_preferences_status(
                current_user["id"], True)
        except Exception as e:
            logger.error(
                f"Erro ao atualizar status das preferências: {str(e)}")
            # Não queremos que isso impeça a criação do plano, então apenas logamos

        logger.info(
            f"Plano criado com sucesso: {plan.id} para usuário {current_user['id']}")
        return plan

    except Exception as e:
        logger.error(f"Erro ao inicializar plano de estudo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao inicializar plano de estudo: {str(e)}"
        )


@study_router.get("/onboarding/status")
async def get_onboarding_status(
    current_user: dict = Depends(get_current_active_user),
    study_service: StudyService = Depends(get_study_service)
):
    """
    Retorna o status do onboarding do usuário.
    Verifica tanto o status no ms-auth (current_user) quanto as preferências no ms-study.
    """
    preferences = study_service.get_user_preferences(current_user["id"])

    # Verificar se existem preferências e se o onboarding está completo
    onboarding_status = {
        "completed": False,
        "has_preferences": False,
        "has_study_plan": False
    }

    # Verificar se o status de onboarding está disponível no objeto current_user
    # Isso é mais confiável porque vem diretamente da tabela users no ms-auth
    if "onboarding_completed" in current_user and current_user["onboarding_completed"]:
        onboarding_status["completed"] = True

    # Como fallback, verificar também nas preferências do usuário
    if preferences:
        onboarding_status["has_preferences"] = True

        # Se o status não foi definido pelo current_user, usar o das preferências
        if not onboarding_status["completed"]:
            onboarding_status["completed"] = preferences.onboarding_completed

        # Verificar se o usuário já tem um plano de estudo
        plans = study_service.get_study_plans_by_user(current_user["id"])
        onboarding_status["has_study_plan"] = len(plans) > 0

    return onboarding_status


@study_router.get("/current-plan", response_model=StudyPlanResponse)
async def get_current_study_plan(
    current_user: dict = Depends(get_current_active_user),
    study_service: StudyService = Depends(get_study_service)
):
    """
    Retorna o plano de estudo atual (mais recente) do usuário.
    Este endpoint é usado pela aplicação frontend para exibir o plano de estudo atual na página Home.
    """
    try:
        # Obter todos os planos do usuário
        plans = study_service.get_study_plans_by_user(current_user["id"])

        if not plans:
            # Se o usuário não tiver planos, retornar 404
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum plano de estudo encontrado para o usuário"
            )

        # Retornar o plano mais recente
        current_plan = max(plans, key=lambda p: p.created_at)

        # Registrar o acesso ao plano para fins de logging
        logger.info(
            f"User {current_user['id']} accessed current study plan {current_plan.id}: {current_plan.title}")

        return current_plan
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e

        logger.error(f"Error getting current study plan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter plano de estudo atual: {str(e)}"
        )
