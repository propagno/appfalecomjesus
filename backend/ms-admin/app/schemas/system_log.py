from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class SystemLogBase(BaseModel):
    level: str
    source: str
    message: str
    details: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None


class SystemLogCreate(SystemLogBase):
    pass


class SystemLogUpdate(BaseModel):
    resolved: bool = True
    resolution_notes: Optional[str] = None


class SystemLog(SystemLogBase):
    id: str
    timestamp: datetime
    resolved: bool
    resolved_by: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None

    class Config:
        from_attributes = True


class SystemLogListResponse(BaseModel):
    items: List[SystemLog]
    total: int
    page: int
    size: int
