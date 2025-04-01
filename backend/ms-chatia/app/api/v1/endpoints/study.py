from typing import Dict, List, Optional, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import httpx
import json
import logging
from datetime import datetime

from app.api.deps import get_current_user, get_db
from app.core.logging import get_logger
from app.schemas.study import (
    StudyPlan,
    StudyPlanCreate,
    StudyPlanUpdate,
    StudyProgress,
    Certificate,
    StudyPlanRequest,
    StudyPlanResponse,
    SessionItem,
    ContentItem
)
from app.services.study_service import StudyService
from app.services.openai_service import OpenAIService
from app.core.config import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)
settings = get_settings()


@router.post(
    "/plans",
    response_model=StudyPlan,
    status_code=status.HTTP_201_CREATED,
    summary="Criar plano de estudo",
    description="""
    Cria um novo plano de estudo personalizado com base nas preferências.
    
    O plano é gerado pela IA considerando:
    - Objetivos espirituais
    - Nível de conhecimento bíblico
    - Formato preferido de conteúdo
    - Horário disponível para estudo
    
    O plano inclui:
    - Título inspirador
    - Descrição detalhada
    - 7 dias de duração
    - 20 minutos por sessão
    - Versículos específicos
    - Reflexões guiadas
    """
)
async def create_study_plan(
    *,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user),
    plan: StudyPlanCreate
) -> StudyPlan:
    """
    Cria um novo plano de estudo personalizado.

    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        plan: Dados do plano a ser criado

    Returns:
        StudyPlan com detalhes do plano criado

    Raises:
        HTTPException: Se erro na criação
    """
    try:
        study_service = StudyService(db)
        return await study_service.create_study_plan(
            user_id=current_user["id"],
            preferences=plan
        )
    except Exception as e:
        logger.error(f"Error creating study plan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar plano de estudo"
        )


@router.get(
    "/plans/{plan_id}",
    response_model=StudyPlan,
    summary="Buscar plano de estudo",
    description="""
    Recupera os detalhes de um plano de estudo específico.
    
    Inclui:
    - Dados do plano
    - Lista de seções
    - Conteúdos de cada seção
    - Status de progresso
    """
)
async def get_study_plan(
    plan_id: UUID,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> StudyPlan:
    """
    Recupera um plano de estudo específico.

    Args:
        plan_id: ID do plano
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        StudyPlan com detalhes do plano

    Raises:
        HTTPException: Se plano não encontrado ou acesso negado
    """
    try:
        study_service = StudyService(db)
        return await study_service.get_study_plan(
            user_id=current_user["id"],
            plan_id=plan_id
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting study plan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao recuperar plano"
        )


@router.get(
    "/plans",
    response_model=List[StudyPlan],
    summary="Listar planos de estudo",
    description="""
    Lista todos os planos de estudo do usuário.
    
    Inclui planos:
    - Em andamento
    - Concluídos
    - Não iniciados
    """
)
async def list_study_plans(
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> List[StudyPlan]:
    """
    Lista todos os planos de estudo do usuário.

    Args:
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Lista de StudyPlan

    Raises:
        HTTPException: Se erro na listagem
    """
    try:
        study_service = StudyService(db)
        return await study_service.list_study_plans(
            user_id=current_user["id"]
        )
    except Exception as e:
        logger.error(f"Error listing study plans: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar planos"
        )


@router.put(
    "/plans/{plan_id}",
    response_model=StudyPlan,
    summary="Atualizar plano de estudo",
    description="""
    Atualiza os dados de um plano de estudo existente.
    
    Permite alterar:
    - Título
    - Descrição
    - Duração total
    - Duração diária
    """
)
async def update_study_plan(
    *,
    plan_id: UUID,
    plan: StudyPlanUpdate,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> StudyPlan:
    """
    Atualiza um plano de estudo existente.

    Args:
        plan_id: ID do plano
        plan: Dados a atualizar
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        StudyPlan atualizado

    Raises:
        HTTPException: Se plano não encontrado ou erro na atualização
    """
    try:
        study_service = StudyService(db)
        return await study_service.update_study_plan(
            user_id=current_user["id"],
            plan_id=plan_id,
            plan_data=plan
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating study plan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar plano"
        )


@router.post(
    "/plans/{plan_id}/sections/{section_id}/progress",
    response_model=StudyProgress,
    summary="Atualizar progresso",
    description="""
    Atualiza o progresso em uma seção do plano.
    
    Marca a seção como concluída e calcula:
    - Progresso total no plano
    - Total de seções concluídas
    - Status geral
    """
)
async def update_section_progress(
    *,
    plan_id: UUID,
    section_id: UUID,
    completed: bool,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> StudyProgress:
    """
    Atualiza o progresso em uma seção do plano.

    Args:
        plan_id: ID do plano
        section_id: ID da seção
        completed: Se foi concluída
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        StudyProgress com status atualizado

    Raises:
        HTTPException: Se seção não encontrada ou erro na atualização
    """
    try:
        study_service = StudyService(db)
        return await study_service.update_progress(
            user_id=current_user["id"],
            plan_id=plan_id,
            section_id=section_id,
            completed=completed
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating progress: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar progresso"
        )


@router.post(
    "/plans/{plan_id}/certificate",
    response_model=Certificate,
    summary="Gerar certificado",
    description="""
    Gera certificado de conclusão do plano.
    
    O certificado inclui:
    - Título do plano
    - Data de conclusão
    - Código único
    - Nome do usuário
    
    Requer que todas as seções estejam concluídas.
    """
)
async def generate_certificate(
    plan_id: UUID,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> Certificate:
    """
    Gera certificado de conclusão do plano.

    Args:
        plan_id: ID do plano
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Certificate com dados do certificado

    Raises:
        HTTPException: Se plano não concluído ou erro na geração
    """
    try:
        study_service = StudyService(db)
        return await study_service.generate_certificate(
            user_id=current_user["id"],
            plan_id=plan_id
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating certificate: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao gerar certificado"
        )


@router.post(
    "/generate-plan",
    response_model=StudyPlanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Gerar plano de estudo personalizado",
    description="""
    Gera um plano de estudo personalizado com base nas preferências do usuário.
    
    Este endpoint:
    1. Recebe as preferências do usuário
    2. Utiliza IA para criar um plano personalizado
    3. Retorna o plano estruturado
    4. Opcionalmente, salva o plano no MS-Study
    
    Requer autenticação.
    """
)
async def generate_study_plan(
    request: StudyPlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Gera um plano de estudo personalizado com IA e integra com MS-Study
    """
    try:
        # Inicializar o serviço OpenAI
        openai_service = OpenAIService()

        # Preparar as preferências para o prompt
        preferences = {
            "objectives": request.objectives,
            "bible_experience_level": request.bible_experience_level,
            "content_preferences": request.content_preferences,
            "preferred_time": request.preferred_time
        }

        # Gerar o plano usando IA
        logger.info(
            f"Gerando plano para o usuário {current_user.id} com objetivos {request.objectives}")
        plan_content = await openai_service.generate_study_plan(current_user.id, preferences)

        # Estruturar o plano gerado
        sessions = []
        for day, session in enumerate(plan_content.get("sections", []), 1):
            contents = []
            for content_item in session.get("contents", []):
                contents.append(ContentItem(
                    content_type=content_item.get("type", "text"),
                    content=content_item.get("content", ""),
                    position=content_item.get("position", 1)
                ))

            sessions.append(SessionItem(
                title=session.get("title", f"Dia {day}"),
                position=day,
                duration_minutes=session.get("duration_minutes", 20),
                contents=contents
            ))

        # Criar a resposta
        response = StudyPlanResponse(
            title=plan_content.get("title", "Plano Personalizado"),
            description=plan_content.get(
                "description", "Plano gerado com base nas suas preferências."),
            duration_days=len(plan_content.get("sections", [])),
            daily_duration_minutes=20,
            objectives=request.objectives,
            bible_experience_level=request.bible_experience_level,
            sessions=sessions
        )

        # Se o salvamento for solicitado, enviar para o MS-Study
        if request.save_in_study_service:
            await save_plan_to_study_service(response, current_user.id)

        return response

    except Exception as e:
        logger.error(f"Erro ao gerar plano de estudo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar plano de estudo: {str(e)}"
        )


@router.get(
    "/study-plan-templates",
    response_model=List[Dict[str, Any]],
    summary="Listar modelos de planos de estudo",
    description="""
    Retorna modelos pré-configurados de planos de estudo.
    
    Estes modelos podem ser usados como base para personalização.
    """
)
async def get_study_plan_templates():
    """
    Retorna modelos de planos pré-configurados que podem ser usados como base
    """
    templates = [
        {
            "id": "template-novatosfe",
            "title": "Primeiros Passos na Fé",
            "description": "Para iniciantes, aborda fundamentos da fé cristã.",
            "duration_days": 7,
            "daily_duration_minutes": 15,
            "objectives": ["crescimento espiritual", "fundamentos da fé"],
            "bible_experience_level": "iniciante"
        },
        {
            "id": "template-ansiedade",
            "title": "Superando a Ansiedade",
            "description": "Encontre paz e tranquilidade através da Palavra.",
            "duration_days": 7,
            "daily_duration_minutes": 20,
            "objectives": ["ansiedade", "paz"],
            "bible_experience_level": "intermediário"
        },
        {
            "id": "template-sabedoria",
            "title": "Em Busca de Sabedoria",
            "description": "Estudo dos livros de sabedoria da Bíblia.",
            "duration_days": 10,
            "daily_duration_minutes": 25,
            "objectives": ["sabedoria", "discernimento"],
            "bible_experience_level": "avançado"
        }
    ]

    return templates


@router.get(
    "/suggested-objectives",
    response_model=List[str],
    summary="Listar objetivos sugeridos",
    description="Retorna uma lista de objetivos espirituais sugeridos para planos de estudo."
)
async def get_suggested_objectives():
    """
    Retorna lista de objetivos espirituais comuns para sugestão ao usuário
    """
    objectives = [
        "ansiedade",
        "paz",
        "sabedoria",
        "crescimento espiritual",
        "gratidão",
        "perdão",
        "paciência",
        "depressão",
        "família",
        "relacionamentos",
        "trabalho",
        "finanças",
        "propósito",
        "fortalecer a fé",
        "conhecer mais a bíblia",
        "oração",
        "comunhão"
    ]

    return objectives


async def save_plan_to_study_service(plan: StudyPlanResponse, user_id: str):
    """
    Salva o plano gerado no MS-Study via API REST

    Args:
        plan: Plano de estudo gerado
        user_id: ID do usuário

    Raises:
        Exception: Se falhar ao salvar o plano
    """
    try:
        # URL do microsserviço MS-Study
        ms_study_url = settings.MS_STUDY_URL

        # Preparar os dados para o formato esperado pelo MS-Study
        study_plan_data = {
            "title": plan.title,
            "description": plan.description,
            "category": ", ".join(plan.objectives),
            "difficulty": plan.bible_experience_level,
            "duration_days": plan.duration_days,
            "daily_duration_minutes": plan.daily_duration_minutes,
            "image_url": None,
            "sections": []
        }

        # Preparar seções do plano
        for session in plan.sessions:
            section_data = {
                "title": session.title,
                "position": session.position,
                "duration_minutes": session.duration_minutes,
                "contents": []
            }

            # Adicionar conteúdos de cada seção
            for content in session.contents:
                content_data = {
                    "content_type": content.content_type,
                    "content": content.content,
                    "position": content.position
                }
                section_data["contents"].append(content_data)

            study_plan_data["sections"].append(section_data)

        # Fazer a requisição para o MS-Study
        async with httpx.AsyncClient() as client:
            headers = {
                "Content-Type": "application/json",
                "X-User-ID": str(user_id)  # Para autenticação entre serviços
            }

            response = await client.post(
                f"{ms_study_url}/api/study-plans/",
                json=study_plan_data,
                headers=headers,
                timeout=30.0
            )

            # Verificar se a resposta foi bem-sucedida
            if response.status_code != 201:
                logger.error(
                    f"Erro ao salvar plano no MS-Study: {response.text}")
                raise Exception(f"Erro ao salvar plano: {response.text}")

            logger.info(
                f"Plano salvo com sucesso no MS-Study para o usuário {user_id}")

            return response.json()

    except httpx.RequestError as e:
        logger.error(f"Erro de conexão com MS-Study: {str(e)}")
        raise Exception(f"Falha de conexão com o serviço de estudos: {str(e)}")

    except Exception as e:
        logger.error(f"Erro ao salvar plano no MS-Study: {str(e)}")
        raise Exception(f"Falha ao salvar plano: {str(e)}")
