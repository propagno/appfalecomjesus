from typing import Optional
from pydantic import BaseModel, Field, UUID4, validator
from datetime import datetime
import uuid


class UserStudyProgressBase(BaseModel):
    """
    Schema base para o progresso de estudo do usuário.
    """
    user_id: UUID4 = Field(..., description="ID do usuário")
    study_plan_id: UUID4 = Field(..., description="ID do plano de estudo")
    current_section_id: Optional[UUID4] = Field(
        None, description="ID da seção atual do usuário")
    completion_percentage: float = Field(
        0.0, description="Porcentagem de conclusão", ge=0.0, le=100.0)


class UserStudyProgressCreate(UserStudyProgressBase):
    """
    Schema para criação de progresso de estudo.
    """
    started_at: Optional[datetime] = Field(
        None, description="Data e hora de início do estudo")


class UserStudyProgressUpdate(BaseModel):
    """
    Schema para atualização de progresso de estudo.
    """
    current_section_id: Optional[UUID4] = Field(
        None, description="ID da seção atual do usuário")
    completion_percentage: Optional[float] = Field(
        None, description="Porcentagem de conclusão", ge=0.0, le=100.0)
    completed_at: Optional[datetime] = Field(
        None, description="Data e hora de conclusão do estudo")

    @validator('completion_percentage')
    def validate_percentage(cls, v):
        if v is not None and (v < 0.0 or v > 100.0):
            raise ValueError(
                'A porcentagem de conclusão deve estar entre 0.0 e 100.0')
        return v


class UserStudyProgressInDB(UserStudyProgressBase):
    """
    Schema para progresso de estudo persistido no banco.
    """
    id: UUID4 = Field(default_factory=uuid.uuid4,
                      description="ID único do progresso")
    started_at: datetime = Field(...,
                                 description="Data e hora de início do estudo")
    completed_at: Optional[datetime] = Field(
        None, description="Data e hora de conclusão do estudo")
    updated_at: datetime = Field(...,
                                 description="Data e hora da última atualização")

    class Config:
        from_attributes = True


class UserStudyProgress(UserStudyProgressInDB):
    """
    Schema para resposta de progresso de estudo.
    """
    pass
