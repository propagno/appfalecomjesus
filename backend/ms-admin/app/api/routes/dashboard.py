from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from ...services import dashboard_service
from ...schemas.dashboard import DashboardData, SystemMetrics
from ...api.deps import get_current_admin_user
from ...schemas.auth import User

router = APIRouter()


@router.get("/", response_model=DashboardData)
async def get_dashboard_data(
    period: str = Query(
        "day", description="Período para os dados ('day', 'week', 'month')"),
    current_user: User = Depends(get_current_admin_user)
) -> DashboardData:
    """
    Obtém os dados para o dashboard administrativo, incluindo:
    - Métricas de usuários
    - Estatísticas de uso
    - Dados de crescimento
    - Estado do sistema

    Este endpoint combina dados de vários microsserviços para fornecer uma visão completa.
    """
    # Validar o período
    if period not in ["day", "week", "month"]:
        raise HTTPException(
            status_code=400, detail="Período inválido. Deve ser 'day', 'week' ou 'month'")

    dashboard_data = await dashboard_service.get_dashboard_data(period)
    return dashboard_data


@router.get("/metrics", response_model=SystemMetrics)
async def get_system_metrics(
    current_user: User = Depends(get_current_admin_user)
) -> SystemMetrics:
    """
    Obtém métricas de desempenho do sistema:
    - Uso de CPU
    - Uso de memória
    - Uso de disco
    - Conexões ativas
    - Tempo médio de resposta
    """
    return await dashboard_service.get_system_metrics()
