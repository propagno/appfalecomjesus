from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional, List
from datetime import datetime
import re
from enum import Enum


class SubscriptionTypeEnum(str, Enum):
    FREE = "free"
    PREMIUM = "premium"


class SubscriptionStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"
    PENDING = "pending"


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    name: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User password")

    @field_validator('password')
    def password_complexity(cls, v):
        """Validate password complexity."""
        if not re.search(r'[A-Za-z]', v) or not re.search(r'[0-9]', v):
            raise ValueError(
                'Password must contain at least one letter and one number')
        return v

    @field_validator('name')
    def name_must_be_valid(cls, v):
        """Validate that name has at least two parts and contains only valid characters."""
        parts = v.split()
        if len(parts) < 2:
            raise ValueError('Full name must include first and last name')

        if not all(re.match(r'^[a-zA-ZÀ-ÿ\s\-]+$', part) for part in parts):
            raise ValueError('Name contains invalid characters')
        return v


class UserInDB(UserBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: str
    created_at: datetime
    is_active: bool
    is_admin: bool = False
    onboarding_completed: bool = False

    class Config:
        from_attributes = True


class UserPreferencesBase(BaseModel):
    objectives: List[str] = Field(...,
                                  description="Lista de objetivos espirituais do usuário")
    bible_experience_level: str = Field(
        ..., description="Nível de experiência com a Bíblia (iniciante, intermediário, avançado)")
    content_preferences: List[str] = Field(
        ..., description="Preferências de formato de conteúdo")
    preferred_time: str = Field(
        ..., description="Horário preferido para estudo (manhã, tarde, noite)")
    onboarding_completed: Optional[bool] = Field(
        False, description="Indica se o processo de onboarding foi concluído")


class UserPreferencesCreate(UserPreferencesBase):
    pass


class UserPreferencesResponse(UserPreferencesBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None


class UserSubscriptionBase(BaseModel):
    subscription_type: SubscriptionTypeEnum = Field(default=SubscriptionTypeEnum.FREE,
                                                    description="Tipo de assinatura (gratuita ou premium)")
    status: SubscriptionStatusEnum = Field(default=SubscriptionStatusEnum.ACTIVE,
                                           description="Status da assinatura")
    payment_gateway: Optional[str] = Field(
        None, description="Gateway de pagamento utilizado")
    expiration_date: Optional[datetime] = Field(
        None, description="Data de expiração da assinatura")


class UserSubscriptionCreate(UserSubscriptionBase):
    user_id: str = Field(...,
                         description="ID do usuário associado à assinatura")


class UserSubscriptionUpdate(BaseModel):
    subscription_type: Optional[SubscriptionTypeEnum] = None
    status: Optional[SubscriptionStatusEnum] = None
    payment_gateway: Optional[str] = None
    expiration_date: Optional[datetime] = None
    last_payment_date: Optional[datetime] = None


class UserSubscriptionResponse(UserSubscriptionBase):
    id: str
    user_id: str
    last_payment_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
