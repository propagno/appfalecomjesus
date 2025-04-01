from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


class UserNote(BaseModel):
    id: str
    user_id: str
    note: str
    created_by: str
    created_at: datetime

    class Config:
        from_attributes = True


class AdminUserBase(BaseModel):
    id: str
    email: EmailStr
    name: str
    is_premium: bool = False
    is_blocked: bool = False
    created_at: datetime
    last_login: Optional[datetime] = None


class AdminUserDetails(AdminUserBase):
    subscription_plan: Optional[str] = None
    subscription_expires: Optional[datetime] = None
    study_plans_count: int
    chat_messages_count: int
    last_active: Optional[datetime] = None
    progress_percentage: Optional[int] = None
    notes: List[UserNote] = []

    class Config:
        from_attributes = True


class AdminUserListItem(AdminUserBase):
    pass

    class Config:
        from_attributes = True


class AdminUserListResponse(BaseModel):
    items: List[AdminUserListItem]
    total: int
    page: int
    size: int


class UserNoteCreate(BaseModel):
    note: str


class UserBlockUpdate(BaseModel):
    is_blocked: bool
