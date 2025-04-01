from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ReportJobRequest(BaseModel):
    """Request to generate a new report."""
    start_date: str
    end_date: str
    type: str  # 'user_activity', 'study_progress', 'chat_usage', 'system_performance'
    custom_params: Optional[Dict[str, Any]] = None


class ReportJobResponse(BaseModel):
    """Response for report generation job."""
    job_id: str
    status: str  # 'pending', 'in_progress', 'completed', 'failed'
    message: Optional[str] = None


class ReportInfo(BaseModel):
    """Information about a complete report."""
    id: str
    type: str
    date_range: Dict[str, str]  # {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
    created_at: datetime
    created_by: str
    size: Optional[int] = None  # Size in bytes
    download_url: str


class ReportListResponse(BaseModel):
    """List of available reports."""
    items: List[ReportInfo]
    total: int
