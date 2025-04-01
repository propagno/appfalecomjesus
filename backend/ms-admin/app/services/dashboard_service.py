import httpx
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
import asyncio
import logging
from ..schemas.dashboard import DashboardData, SystemMetrics, MetricCount, GrowthData
from ..crud import system_log

# URLs dos microsserviços
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://ms-auth:5000")
STUDY_SERVICE_URL = os.getenv("STUDY_SERVICE_URL", "http://ms-study:5000")
CHAT_SERVICE_URL = os.getenv("CHAT_SERVICE_URL", "http://ms-chatia:5000")
BIBLE_SERVICE_URL = os.getenv("BIBLE_SERVICE_URL", "http://ms-bible:5000")

logger = logging.getLogger("ms-admin")


async def get_dashboard_data(period: str = "day") -> DashboardData:
    """
    Obtém dados para o dashboard administrativo.

    Args:
        period: Período para os dados de crescimento ('day', 'week', 'month')

    Returns:
        DashboardData
    """
    # Cria tasks para chamadas assíncronas aos outros microsserviços
    tasks = [
        get_user_metrics(),
        get_study_metrics(),
        get_chat_metrics(),
        get_bible_metrics(),
        get_system_health(),
        get_growth_data(period)
    ]

    # Executa as chamadas em paralelo
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Processa os resultados
    user_metrics = results[0] if not isinstance(results[0], Exception) else {
        "total": 0, "active": 0}
    study_metrics = results[1] if not isinstance(results[1], Exception) else {
        "active_plans": 0, "completed_plans": 0}
    chat_metrics = results[2] if not isinstance(results[2], Exception) else {
        "messages_today": 0, "average_per_user": 0}
    bible_metrics = results[3] if not isinstance(results[3], Exception) else 0
    system_health = results[4] if not isinstance(
        results[4], Exception) else "warning"
    growth_data = results[5] if not isinstance(
        results[5], Exception) else ([], [])

    # Se alguma das chamadas falhou, registramos na saída
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(
                f"Erro ao obter métricas para o dashboard: {str(result)}")

    # Retorna os dados do dashboard
    return DashboardData(
        users=MetricCount(**user_metrics),
        studies=study_metrics,
        chat=chat_metrics,
        bible_views=bible_metrics,
        system_health=system_health,
        alerts=await get_alert_count(),
        response_time_ms=200,  # Valor padrão ou calculado com base nas chamadas
        daily_growth=growth_data[0],
        monthly_growth=growth_data[1]
    )


async def get_user_metrics() -> Dict[str, int]:
    """Obtém métricas de usuários do MS-Auth"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{AUTH_SERVICE_URL}/api/auth/metrics/users")
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(
                    f"Erro ao obter métricas de usuários: {response.status_code}")
                return {"total": 0, "active": 0, "premium": 0}
    except Exception as e:
        logger.error(f"Erro na comunicação com MS-Auth: {str(e)}")
        return {"total": 0, "active": 0, "premium": 0}


async def get_study_metrics() -> Dict[str, int]:
    """Obtém métricas de estudos do MS-Study"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{STUDY_SERVICE_URL}/api/study/metrics")
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(
                    f"Erro ao obter métricas de estudos: {response.status_code}")
                return {"active_plans": 0, "completed_plans": 0}
    except Exception as e:
        logger.error(f"Erro na comunicação com MS-Study: {str(e)}")
        return {"active_plans": 0, "completed_plans": 0}


async def get_chat_metrics() -> Dict[str, Any]:
    """Obtém métricas do chat do MS-ChatIA"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{CHAT_SERVICE_URL}/api/chat/metrics")
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(
                    f"Erro ao obter métricas do chat: {response.status_code}")
                return {"messages_today": 0, "average_per_user": 0}
    except Exception as e:
        logger.error(f"Erro na comunicação com MS-ChatIA: {str(e)}")
        return {"messages_today": 0, "average_per_user": 0}


async def get_bible_metrics() -> int:
    """Obtém métricas da Bíblia do MS-Bible"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{BIBLE_SERVICE_URL}/api/bible/metrics/views")
            if response.status_code == 200:
                data = response.json()
                return data.get("total_views", 0)
            else:
                logger.warning(
                    f"Erro ao obter métricas da Bíblia: {response.status_code}")
                return 0
    except Exception as e:
        logger.error(f"Erro na comunicação com MS-Bible: {str(e)}")
        return 0


async def get_system_health() -> str:
    """Verifica a saúde geral do sistema"""
    services_status = []

    # Verifica cada serviço
    services = [
        ("ms-auth", AUTH_SERVICE_URL),
        ("ms-study", STUDY_SERVICE_URL),
        ("ms-chatia", CHAT_SERVICE_URL),
        ("ms-bible", BIBLE_SERVICE_URL)
    ]

    for name, url in services:
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(f"{url}/health")
                services_status.append(response.status_code == 200)
        except Exception:
            services_status.append(False)

    # Determina o status do sistema
    if all(services_status):
        return "healthy"
    elif sum(services_status) >= len(services_status) * 0.75:
        return "warning"
    else:
        return "critical"


async def get_alert_count() -> int:
    """
    Obtém o número de alertas não resolvidos (logs críticos ou erros)
    """
    # Aqui você buscaria do banco de dados
    from sqlalchemy.orm import Session
    from ..db.session import SessionLocal

    db = SessionLocal()
    try:
        # Consulta logs críticos ou erros não resolvidos
        count = db.query(SystemLog).filter(
            SystemLog.level.in_(["error", "critical"]),
            SystemLog.resolved == False
        ).count()
        return count
    except Exception as e:
        logger.error(f"Erro ao obter contagem de alertas: {str(e)}")
        return 0
    finally:
        db.close()


async def get_growth_data(period: str) -> tuple[List[GrowthData], List[GrowthData]]:
    """
    Obtém dados de crescimento diário e mensal

    Args:
        period: 'day', 'week', 'month'

    Returns:
        Tupla com (daily_growth, monthly_growth)
    """
    # Aqui você faria consultas aos serviços para obter dados históricos
    # Para este exemplo, vamos criar dados simulados

    today = date.today()

    # Dados de crescimento diário (últimos 7 ou 30 dias, dependendo do período)
    days = 7 if period == "week" else (30 if period == "month" else 7)
    daily_growth = []

    for i in range(days):
        day_date = today - timedelta(days=days-i-1)
        daily_growth.append(GrowthData(
            date=day_date,
            value=100 + i * 5  # Valor simulado
        ))

    # Dados de crescimento mensal (últimos 12 meses)
    monthly_growth = []
    for i in range(12):
        # Obtém o mesmo dia, mas meses anteriores
        month_date = (today.replace(day=1) - timedelta(days=1)
                      ).replace(day=today.day)
        month_date = month_date.replace(month=(today.month - i) % 12 or 12,
                                        year=today.year - ((today.month - i - 1) // 12))

        monthly_growth.append(GrowthData(
            date=month_date,
            value=500 + i * 50  # Valor simulado
        ))

    return daily_growth, monthly_growth


async def get_system_metrics() -> SystemMetrics:
    """
    Obtém métricas de desempenho do sistema
    """
    # Em um ambiente real, você obteria essas métricas do sistema
    # Por enquanto, simulamos os valores

    return SystemMetrics(
        cpu_usage=30.5,
        memory_usage=45.2,
        disk_usage=60.0,
        active_connections=120,
        response_time_ms=45
    )
