from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    id: Optional[int] = None
    is_active: Optional[bool] = None
    is_superuser: bool = False
