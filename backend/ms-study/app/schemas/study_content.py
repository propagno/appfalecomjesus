from typing import Optional, List
from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from enum import Enum
import uuid


class ContentType(str, Enum):
    TEXT = "text"
    AUDIO = "audio"
    VIDEO = "video"
    IMAGE = "image"
    BIBLE_VERSE = "bible_verse"


class StudyContentBase(BaseModel):
    """
    Schema base para conteúdos de estudo.
    """
    section_id: UUID4 = Field(...,
                              description="ID da seção a qual o conteúdo pertence")
    content_type: ContentType = Field(..., description="Tipo do conteúdo")
    content: str = Field(...,
                         description="Conteúdo em si ou URL para recursos")
    position: int = Field(
        0, description="Posição do conteúdo na sequência da seção")


class StudyContentCreate(StudyContentBase):
    """
    Schema para criação de conteúdos de estudo.
    """
    pass


class StudyContentUpdate(BaseModel):
    """
    Schema para atualização de conteúdos de estudo.
    """
    content_type: Optional[ContentType] = Field(
        None, description="Tipo do conteúdo")
    content: Optional[str] = Field(
        None, description="Conteúdo em si ou URL para recursos")
    position: Optional[int] = Field(
        None, description="Posição do conteúdo na sequência da seção")


class StudyContentInDB(StudyContentBase):
    """
    Schema para conteúdos de estudo persistidos no banco.
    """
    id: UUID4 = Field(default_factory=uuid.uuid4,
                      description="ID único do conteúdo")
    created_at: datetime = Field(...,
                                 description="Data e hora de criação do conteúdo")
    updated_at: Optional[datetime] = Field(
        None, description="Data e hora da última atualização")

    class Config:
        from_attributes = True


class StudyContent(StudyContentInDB):
    """
    Schema para resposta de conteúdos de estudo.
    """
    pass
