from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date


class MetricCount(BaseModel):
    total: int
    active: int
    inactive: Optional[int] = None
    premium: Optional[int] = None


class SystemMetrics(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    active_connections: int
    response_time_ms: int


class GrowthData(BaseModel):
    date: date
    value: int


class DashboardData(BaseModel):
    users: MetricCount
    studies: Dict[str, int]
    chat: Dict[str, Any]
    bible_views: int
    system_health: str  # healthy, warning, critical
    alerts: int
    response_time_ms: int
    daily_growth: List[GrowthData]
    monthly_growth: List[GrowthData]
