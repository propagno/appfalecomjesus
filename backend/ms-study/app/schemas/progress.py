from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

# Schemas para UserStudyProgress


class UserStudyProgressBase(BaseModel):
    user_id: str = Field(..., description="ID do usuário")
    study_plan_id: str = Field(..., description="ID do plano de estudo")
    current_section_id: Optional[str] = Field(
        None, description="ID da seção atual")
    completion_percentage: float = Field(
        0.0, description="Porcentagem de conclusão")


class UserStudyProgressCreate(UserStudyProgressBase):
    pass


class UserStudyProgressUpdate(BaseModel):
    current_section_id: Optional[str] = None
    completion_percentage: Optional[float] = None
    last_activity_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class UserStudyProgressInDB(UserStudyProgressBase):
    id: str
    last_activity_date: datetime
    started_at: datetime
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Schemas para detalhes do progresso incluindo informações do plano


class UserStudyProgressDetail(UserStudyProgressInDB):
    plan_title: str
    plan_description: Optional[str] = None
    plan_duration_days: int
    plan_category: Optional[str] = None
    plan_difficulty: Optional[str] = None
    current_section_title: Optional[str] = None
    current_section_position: Optional[int] = None
    total_sections: int

# Schemas para Reflection (reflexões do usuário)


class ReflectionBase(BaseModel):
    user_id: str = Field(..., description="ID do usuário")
    section_id: str = Field(..., description="ID da seção")
    reflection_text: str = Field(..., description="Texto da reflexão")


class ReflectionCreate(ReflectionBase):
    pass


class ReflectionUpdate(BaseModel):
    reflection_text: str = Field(...,
                                 description="Texto atualizado da reflexão")


class ReflectionInDB(ReflectionBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Schema para detalhes da reflexão incluindo informações da seção


class ReflectionDetail(ReflectionInDB):
    section_title: str
    plan_id: str
    plan_title: str

# Schema para resposta de listagem de reflexões


class ReflectionListResponse(BaseModel):
    items: List[ReflectionDetail]
    total: int
    page: int
    page_size: int

# Schema para resposta de listagem de progressos


class UserStudyProgressListResponse(BaseModel):
    items: List[UserStudyProgressDetail]
    total: int
    page: int
    page_size: int
