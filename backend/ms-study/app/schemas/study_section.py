from typing import Optional, List
from pydantic import BaseModel, Field, UUID4
from datetime import datetime
import uuid
from app.schemas.study_content import StudyContent


class StudySectionBase(BaseModel):
    """
    Schema base para seções de estudo.
    """
    study_plan_id: UUID4 = Field(...,
                                 description="ID do plano de estudo a qual a seção pertence")
    title: str = Field(..., description="Título da seção")
    position: int = Field(
        0, description="Posição da seção na sequência do plano")
    duration_minutes: int = Field(...,
                                  description="Duração estimada em minutos")


class StudySectionCreate(StudySectionBase):
    """
    Schema para criação de seções de estudo.
    """
    pass


class StudySectionUpdate(BaseModel):
    """
    Schema para atualização de seções de estudo.
    """
    title: Optional[str] = Field(None, description="Título da seção")
    position: Optional[int] = Field(
        None, description="Posição da seção na sequência do plano")
    duration_minutes: Optional[int] = Field(
        None, description="Duração estimada em minutos")


class StudySectionInDB(StudySectionBase):
    """
    Schema para seções de estudo persistidas no banco.
    """
    id: UUID4 = Field(default_factory=uuid.uuid4,
                      description="ID único da seção")
    created_at: datetime = Field(...,
                                 description="Data e hora de criação da seção")
    updated_at: Optional[datetime] = Field(
        None, description="Data e hora da última atualização")

    class Config:
        from_attributes = True


class StudySection(StudySectionInDB):
    """
    Schema para resposta de seções de estudo.
    """
    pass


class StudySectionWithContent(StudySection):
    """
    Schema para resposta de seções de estudo com seus conteúdos.
    """
    contents: List[StudyContent] = Field(
        default_factory=list, description="Conteúdos da seção")
