from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

# Schemas para StudyContent


class StudyContentBase(BaseModel):
    content_type: str = Field(...,
                              description="Tipo do conteúdo (texto, áudio, vídeo, etc)")
    content: str = Field(..., description="Conteúdo ou URL")
    position: int = Field(..., description="Posição do conteúdo na seção")
    title: Optional[str] = Field(
        None, description="Título opcional do conteúdo")


class StudyContentCreate(StudyContentBase):
    pass


class StudyContentUpdate(BaseModel):
    content_type: Optional[str] = None
    content: Optional[str] = None
    position: Optional[int] = None
    title: Optional[str] = None


class StudyContentInDB(StudyContentBase):
    id: str
    section_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Schemas para StudySection


class StudySectionBase(BaseModel):
    title: str = Field(..., description="Título da seção")
    description: Optional[str] = Field(None, description="Descrição da seção")
    position: int = Field(..., description="Posição da seção no plano")
    duration_minutes: int = Field(
        20, description="Duração estimada em minutos")
    bible_reference: Optional[str] = Field(
        None, description="Referência bíblica principal")


class StudySectionCreate(StudySectionBase):
    contents: Optional[List[StudyContentCreate]] = Field(
        [], description="Conteúdos da seção")


class StudySectionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    position: Optional[int] = None
    duration_minutes: Optional[int] = None
    bible_reference: Optional[str] = None


class StudySectionInDB(StudySectionBase):
    id: str
    study_plan_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    contents: List[StudyContentInDB] = []

    class Config:
        orm_mode = True

# Schemas para StudyPlan


class StudyPlanBase(BaseModel):
    title: str = Field(..., description="Título do plano")
    description: Optional[str] = Field(None, description="Descrição do plano")
    category: Optional[str] = Field(None, description="Categoria do plano")
    difficulty: Optional[str] = Field(
        None, description="Dificuldade (iniciante, intermediário, avançado)")
    duration_days: int = Field(7, description="Duração em dias")
    image_url: Optional[str] = Field(None, description="URL da imagem de capa")
    is_public: bool = Field(False, description="Se é um plano público")


class StudyPlanCreate(StudyPlanBase):
    user_id: Optional[str] = Field(
        None, description="ID do usuário (null se plano geral)")
    created_by_ia: bool = Field(False, description="Se foi gerado pela IA")
    sections: Optional[List[StudySectionCreate]] = Field(
        [], description="Seções do plano")


class StudyPlanUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    duration_days: Optional[int] = None
    image_url: Optional[str] = None
    is_public: Optional[bool] = None


class StudyPlanInDB(StudyPlanBase):
    id: str
    user_id: Optional[str] = None
    created_by_ia: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    sections: List[StudySectionInDB] = []

    class Config:
        orm_mode = True

# Schema para visualização simplificada do plano


class StudyPlanSimple(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    duration_days: int
    image_url: Optional[str] = None
    created_at: datetime
    sections_count: int = 0

    class Config:
        orm_mode = True

# Schema para listagem de planos


class StudyPlanListResponse(BaseModel):
    items: List[StudyPlanSimple]
    total: int
    page: int
    page_size: int
