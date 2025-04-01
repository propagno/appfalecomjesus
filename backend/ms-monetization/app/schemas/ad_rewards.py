from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class AdRewardBase(BaseModel):
    message_bonus: int
    ad_provider: str
    watched_at: datetime


class AdRewardCreate(AdRewardBase):
    user_id: UUID


class AdRewardResponse(AdRewardBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
