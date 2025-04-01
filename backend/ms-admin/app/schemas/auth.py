from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class TokenPayload(BaseModel):
    sub: str
    exp: int
    is_admin: bool = False


class User(BaseModel):
    id: str
    email: EmailStr
    name: str
    is_admin: bool = False
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
