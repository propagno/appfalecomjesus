from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class BackupJobBase(BaseModel):
    """Base model for backup job information."""
    pass


class BackupJobCreate(BackupJobBase):
    """Model for creating a new backup job."""
    description: Optional[str] = None
    include_files: bool = True
    include_database: bool = True


class BackupJobResponse(BaseModel):
    """Response model for backup job creation or status check."""
    job_id: str
    status: str
    message: Optional[str] = None
    progress: Optional[int] = None
    download_url: Optional[str] = None


class BackupInfo(BaseModel):
    """Information about a complete backup."""
    id: str
    date: datetime
    size: int  # Size in bytes
    description: Optional[str] = None
    created_by: str
    download_url: str
    includes_files: bool
    includes_database: bool


class BackupListResponse(BaseModel):
    """List of backups response."""
    items: List[BackupInfo]
    total: int
