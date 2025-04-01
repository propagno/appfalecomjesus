from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime


class UserBase(BaseModel):
    """
    Schema base para usuários.
    """
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False


class UserCreate(UserBase):
    """
    Schema para criação de usuários.
    """
    password: str


class UserUpdate(UserBase):
    """
    Schema para atualização de usuários.
    """
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    """
    Schema para usuário no banco de dados.
    """
    id: str

    class Config:
        orm_mode = True


class User(UserBase):
    """
    Schema para resposta de usuário.
    """
    id: str
    subscription_plan: Optional[str] = None
    subscription_end_date: Optional[datetime] = None

    class Config:
        orm_mode = True
