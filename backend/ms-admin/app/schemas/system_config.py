from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SystemConfigBase(BaseModel):
    key: str
    value: str
    description: Optional[str] = None
    is_sensitive: bool = False
    category: Optional[str] = None


class SystemConfigCreate(SystemConfigBase):
    pass


class SystemConfigUpdate(BaseModel):
    value: str
    description: Optional[str] = None


class SystemConfig(SystemConfigBase):
    id: str
    updated_at: datetime
    updated_by: str

    class Config:
        from_attributes = True


class SystemConfigListResponse(BaseModel):
    items: List[SystemConfig]
    total: int
