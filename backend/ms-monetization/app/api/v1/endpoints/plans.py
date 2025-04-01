from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.core.database import get_db
from app.schemas.plan import PlanResponse, PlanListResponse
from app.services.plan import PlanService
from typing import Dict, List

router = APIRouter()


@router.get(
    "/plans",
    response_model=PlanListResponse,
    status_code=status.HTTP_200_OK,
    summary="Lista todos os planos disponíveis",
    description="""
    Retorna a lista completa de planos disponíveis para assinatura.
    Inclui informações detalhadas sobre:
    - Nome e descrição do plano
    - Preço mensal e anual
    - Recursos incluídos
    - Limitações (se houver)
    """,
    responses={
        200: {
            "description": "Lista de planos obtida com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "plans": [{
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "name": "Premium",
                            "description": "Acesso ilimitado a todos os recursos",
                            "price_monthly": 29.90,
                            "price_yearly": 299.90,
                            "features": [
                                "Chat IA ilimitado",
                                "Estudos personalizados",
                                "Sem anúncios"
                            ]
                        }]
                    }
                }
            }
        }
    }
)
async def list_plans(
    db: Session = Depends(get_db)
) -> Dict:
    """
    Lista todos os planos disponíveis para assinatura.
    """
    return await PlanService.get_all_plans(db)


@router.get(
    "/plans/{plan_id}",
    response_model=PlanResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtém detalhes de um plano específico",
    description="""
    Retorna informações detalhadas sobre um plano específico.
    Inclui preços, recursos, limitações e condições especiais.
    """,
    responses={
        200: {
            "description": "Detalhes do plano obtidos com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "Premium",
                        "description": "Acesso ilimitado a todos os recursos",
                        "price_monthly": 29.90,
                        "price_yearly": 299.90,
                        "features": [
                            "Chat IA ilimitado",
                            "Estudos personalizados",
                            "Sem anúncios"
                        ]
                    }
                }
            }
        },
        404: {
            "description": "Plano não encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Plan not found"
                    }
                }
            }
        }
    }
)
async def get_plan(
    plan_id: str,
    db: Session = Depends(get_db)
) -> Dict:
    """
    Obtém detalhes de um plano específico.
    """
    plan = await PlanService.get_plan_by_id(db, plan_id)
    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Plan not found"
        )
    return plan


@router.get(
    "/plans/compare",
    response_model=PlanListResponse,
    status_code=status.HTTP_200_OK,
    summary="Compara os planos disponíveis",
    description="""
    Retorna uma comparação detalhada entre todos os planos disponíveis.
    Útil para ajudar o usuário a escolher o plano mais adequado.
    """,
    responses={
        200: {
            "description": "Comparação de planos obtida com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "plans": [
                            {
                                "id": "123e4567-e89b-12d3-a456-426614174000",
                                "name": "Free",
                                "description": "Acesso básico",
                                "price_monthly": 0,
                                "price_yearly": 0,
                                "features": [
                                    "5 mensagens/dia no chat IA",
                                    "10 dias de estudo/mês",
                                    "Com anúncios"
                                ]
                            },
                            {
                                "id": "123e4567-e89b-12d3-a456-426614174001",
                                "name": "Premium",
                                "description": "Acesso ilimitado",
                                "price_monthly": 29.90,
                                "price_yearly": 299.90,
                                "features": [
                                    "Chat IA ilimitado",
                                    "Estudos ilimitados",
                                    "Sem anúncios"
                                ]
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def compare_plans(
    db: Session = Depends(get_db)
) -> Dict:
    """
    Retorna uma comparação detalhada entre todos os planos disponíveis.
    """
    return await PlanService.get_all_plans(db)
