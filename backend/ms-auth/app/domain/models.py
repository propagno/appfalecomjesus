import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    password_hash: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserPreferences(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    objectives: List[str]
    bible_experience_level: str
    content_preferences: List[str]
    preferred_time: str
    onboarding_completed: bool
    created_at: datetime

    class Config:
        orm_mode = True


class UserSubscription(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    plan_type: str  # "Free", "Premium"
    subscription_status: str  # "active", "inactive", "canceled"
    payment_gateway: Optional[str]
    expiration_date: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True
