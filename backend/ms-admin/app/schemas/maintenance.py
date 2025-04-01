from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MaintenanceTaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    scheduled_for: Optional[datetime] = None
    assigned_to: Optional[str] = None
    is_automatic: bool = False
    priority: str = "medium"
    task_type: str


class MaintenanceTaskCreate(MaintenanceTaskBase):
    pass


class MaintenanceTaskUpdate(BaseModel):
    status: str
    error_message: Optional[str] = None
    completed_at: Optional[datetime] = None


class MaintenanceTask(MaintenanceTaskBase):
    id: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: str
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


class MaintenanceTaskListResponse(BaseModel):
    items: List[MaintenanceTask]
    total: int
    page: int
    size: int
