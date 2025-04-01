from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class StudyContentBase(BaseModel):
    """Schema base para conteúdo de estudo"""
    content_type: str = Field(...,
                              description="Tipo do conteúdo (text, audio, video)")
    content: str = Field(..., description="Conteúdo em si")
    position: int = Field(..., description="Posição na seção")


class StudyContentCreate(StudyContentBase):
    """Schema para criação de conteúdo"""
    pass


class StudyContentResponse(StudyContentBase):
    """Schema para resposta de conteúdo"""
    id: str
    section_id: str
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "section_id": "123e4567-e89b-12d3-a456-426614174001",
                "content_type": "text",
                "content": "Versículo do dia: João 3:16",
                "position": 1,
                "created_at": "2024-03-23T10:00:00Z"
            }
        }


class StudySectionBase(BaseModel):
    """Schema base para seção de estudo"""
    title: str = Field(..., description="Título da seção")
    position: int = Field(..., description="Posição no plano")
    duration_minutes: int = Field(..., description="Duração em minutos")


class StudySectionCreate(StudySectionBase):
    """Schema para criação de seção"""
    pass


class StudySectionResponse(StudySectionBase):
    """Schema para resposta de seção"""
    id: str
    study_plan_id: str
    created_at: datetime
    contents: List[StudyContentResponse] = []

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174001",
                "study_plan_id": "123e4567-e89b-12d3-a456-426614174002",
                "title": "Dia 1: Introdução",
                "position": 1,
                "duration_minutes": 20,
                "created_at": "2024-03-23T10:00:00Z",
                "contents": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "section_id": "123e4567-e89b-12d3-a456-426614174001",
                        "content_type": "text",
                        "content": "Versículo do dia: João 3:16",
                        "position": 1,
                        "created_at": "2024-03-23T10:00:00Z"
                    }
                ]
            }
        }


class StudyPlanBase(BaseModel):
    """Schema base para plano de estudo"""
    title: str = Field(..., description="Título do plano")
    description: str = Field(..., description="Descrição do plano")
    duration_days: int = Field(..., description="Duração em dias")


class StudyPlanCreate(StudyPlanBase):
    """Schema para criação de plano"""
    pass


class StudyPlanResponse(StudyPlanBase):
    """Schema para resposta de plano"""
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    sections: List[StudySectionResponse] = []

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174002",
                "user_id": "123e4567-e89b-12d3-a456-426614174003",
                "title": "Paz Interior com João",
                "description": "Plano de 7 dias focado em encontrar paz interior",
                "duration_days": 7,
                "created_at": "2024-03-23T10:00:00Z",
                "sections": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174001",
                        "study_plan_id": "123e4567-e89b-12d3-a456-426614174002",
                        "title": "Dia 1: Introdução",
                        "position": 1,
                        "duration_minutes": 20,
                        "created_at": "2024-03-23T10:00:00Z",
                        "contents": [
                            {
                                "id": "123e4567-e89b-12d3-a456-426614174000",
                                "section_id": "123e4567-e89b-12d3-a456-426614174001",
                                "content_type": "text",
                                "content": "Versículo do dia: João 3:16",
                                "position": 1,
                                "created_at": "2024-03-23T10:00:00Z"
                            }
                        ]
                    }
                ]
            }
        }


class UserStudyProgressBase(BaseModel):
    """Schema base para progresso do usuário"""
    study_plan_id: str = Field(..., description="ID do plano de estudo")
    current_section_id: Optional[str] = Field(
        None, description="ID da seção atual")
    completion_percentage: float = Field(...,
                                         description="Porcentagem de conclusão")


class UserStudyProgressCreate(UserStudyProgressBase):
    """Schema para criação de progresso"""
    pass


class UserStudyProgressResponse(UserStudyProgressBase):
    """Schema para resposta de progresso"""
    id: str
    user_id: str
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174004",
                "user_id": "123e4567-e89b-12d3-a456-426614174003",
                "study_plan_id": "123e4567-e89b-12d3-a456-426614174002",
                "current_section_id": "123e4567-e89b-12d3-a456-426614174001",
                "completion_percentage": 25.5,
                "updated_at": "2024-03-23T10:00:00Z"
            }
        }
