from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field


class StudyContentBase(BaseModel):
    """
    Schema base para conteúdo de estudo.

    Attributes:
        content_type: Tipo do conteúdo (texto, áudio)
        content: Conteúdo em si ou URL
        position: Ordem na seção
    """
    content_type: str = Field(
        ...,
        description="Tipo do conteúdo",
        example="texto"
    )
    content: str = Field(
        ...,
        description="Conteúdo ou URL do recurso",
        example="João 3:16 - Porque Deus amou o mundo..."
    )
    position: int = Field(
        ...,
        description="Ordem na seção",
        example=1,
        ge=1
    )


class StudyContentCreate(StudyContentBase):
    """Schema para criar novo conteúdo."""
    pass


class StudyContentUpdate(StudyContentBase):
    """Schema para atualizar conteúdo existente."""
    pass


class StudyContent(StudyContentBase):
    """
    Schema completo de conteúdo com dados adicionais.

    Attributes:
        id: Identificador único
        section_id: ID da seção pai
        created_at: Data de criação
    """
    id: UUID
    section_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class StudySectionBase(BaseModel):
    """
    Schema base para seção de estudo.

    Attributes:
        title: Título da seção
        position: Ordem no plano
        duration_minutes: Duração estimada
    """
    title: str = Field(
        ...,
        description="Título da seção",
        example="Encontrando Paz em João 14",
        max_length=255
    )
    position: int = Field(
        ...,
        description="Ordem no plano",
        example=1,
        ge=1
    )
    duration_minutes: int = Field(
        ...,
        description="Duração estimada em minutos",
        example=20,
        ge=5,
        le=120
    )


class StudySectionCreate(StudySectionBase):
    """
    Schema para criar nova seção.

    Attributes:
        contents: Lista de conteúdos
    """
    contents: List[StudyContentCreate]


class StudySectionUpdate(StudySectionBase):
    """
    Schema para atualizar seção existente.

    Attributes:
        completed: Se foi concluída
    """
    completed: Optional[bool] = Field(
        None,
        description="Status de conclusão"
    )


class StudySection(StudySectionBase):
    """
    Schema completo de seção com dados adicionais.

    Attributes:
        id: Identificador único
        study_plan_id: ID do plano pai
        completed: Se foi concluída
        completed_at: Data de conclusão
        contents: Lista de conteúdos
    """
    id: UUID
    study_plan_id: UUID
    completed: bool
    completed_at: Optional[datetime]
    contents: List[StudyContent]

    class Config:
        from_attributes = True


class StudyPlanBase(BaseModel):
    """
    Schema base para plano de estudo.

    Attributes:
        title: Título inspirador
        description: Descrição detalhada
        duration_days: Duração total
        daily_duration: Duração diária
    """
    title: str = Field(
        ...,
        description="Título inspirador do plano",
        example="Jornada de Paz e Sabedoria",
        max_length=255
    )
    description: str = Field(
        ...,
        description="Descrição detalhada",
        example="Um plano para encontrar paz...",
        max_length=1000
    )
    duration_days: int = Field(
        ...,
        description="Duração total em dias",
        example=7,
        ge=1,
        le=90
    )
    daily_duration: int = Field(
        ...,
        description="Duração diária em minutos",
        example=20,
        ge=5,
        le=120
    )


class StudyPlanCreate(StudyPlanBase):
    """
    Schema para criar novo plano.

    Attributes:
        sections: Lista de seções
    """
    sections: List[StudySectionCreate]


class StudyPlanUpdate(StudyPlanBase):
    """Schema para atualizar plano existente."""
    pass


class StudyPlan(StudyPlanBase):
    """
    Schema completo de plano com dados adicionais.

    Attributes:
        id: Identificador único
        user_id: ID do usuário dono
        created_at: Data de criação
        completed_at: Data de conclusão
        sections: Lista de seções
    """
    id: UUID
    user_id: UUID
    created_at: datetime
    completed_at: Optional[datetime]
    sections: List[StudySection]

    class Config:
        from_attributes = True


class StudyProgress(BaseModel):
    """
    Schema para progresso no plano.

    Attributes:
        completed: Se a seção foi concluída
        progress: Porcentagem total
        total_sections: Total de seções
        completed_sections: Seções concluídas
    """
    completed: bool = Field(
        ...,
        description="Status da seção atual"
    )
    progress: float = Field(
        ...,
        description="Progresso total (%)",
        example=42.5,
        ge=0,
        le=100
    )
    total_sections: int = Field(
        ...,
        description="Total de seções",
        example=7,
        ge=1
    )
    completed_sections: int = Field(
        ...,
        description="Seções concluídas",
        example=3,
        ge=0
    )


class Certificate(BaseModel):
    """
    Schema para certificado de conclusão.

    Attributes:
        user_id: ID do usuário
        plan_id: ID do plano
        plan_title: Título do plano
        completion_date: Data de conclusão
        certificate_code: Código único
    """
    user_id: UUID
    plan_id: UUID
    plan_title: str = Field(
        ...,
        description="Título do plano concluído"
    )
    completion_date: datetime = Field(
        ...,
        description="Data de conclusão"
    )
    certificate_code: str = Field(
        ...,
        description="Código único do certificado",
        example="CERT-abc123"
    )


class ContentItem(BaseModel):
    """
    Um item de conteúdo de uma sessão de estudo
    """
    content_type: str = Field(
        ...,
        title="Tipo",
        description="Tipo de conteúdo (texto, verso, reflexão, oração, áudio)",
        example="verse"
    )
    content: str = Field(
        ...,
        title="Conteúdo",
        description="Conteúdo textual ou URL para áudio/imagem",
        example="João 3:16 - Porque Deus amou o mundo de tal maneira..."
    )
    position: int = Field(
        ...,
        title="Posição",
        description="Ordem de exibição do conteúdo na sessão",
        example=1
    )


class SessionItem(BaseModel):
    """
    Uma sessão de estudo (geralmente um dia)
    """
    title: str = Field(
        ...,
        title="Título",
        description="Título da sessão do plano",
        example="Dia 1: Paz em Cristo"
    )
    position: int = Field(
        ...,
        title="Posição",
        description="Ordem da sessão no plano (geralmente representa o dia)",
        example=1
    )
    duration_minutes: int = Field(
        ...,
        title="Duração",
        description="Duração estimada em minutos",
        example=20
    )
    contents: List[ContentItem] = Field(
        ...,
        title="Conteúdos",
        description="Lista de conteúdos da sessão"
    )


class StudyPlanRequest(BaseModel):
    """
    Requisição para gerar um plano de estudo personalizado
    """
    objectives: List[str] = Field(
        ...,
        title="Objetivos",
        description="Objetivos espirituais do usuário",
        min_items=1,
        max_items=5,
        example=["ansiedade", "sabedoria"]
    )
    bible_experience_level: str = Field(
        ...,
        title="Nível",
        description="Nível de experiência com a Bíblia",
        example="iniciante"
    )
    content_preferences: List[str] = Field(
        ...,
        title="Preferências",
        description="Tipos de conteúdo preferidos",
        example=["texto", "áudio"]
    )
    preferred_time: str = Field(
        ...,
        title="Horário",
        description="Horário preferido para estudo",
        example="manhã"
    )
    save_in_study_service: bool = Field(
        False,
        title="Salvar",
        description="Se deve salvar o plano no MS-Study para uso posterior"
    )


class StudyPlanResponse(BaseModel):
    """
    Resposta com o plano de estudo gerado
    """
    title: str = Field(
        ...,
        title="Título",
        description="Título do plano gerado",
        example="Encontrando Paz em Cristo"
    )
    description: str = Field(
        ...,
        title="Descrição",
        description="Descrição detalhada do plano",
        example="Um plano de 7 dias para superar a ansiedade através dos ensinamentos de Jesus."
    )
    duration_days: int = Field(
        ...,
        title="Duração",
        description="Duração total do plano em dias",
        example=7
    )
    daily_duration_minutes: int = Field(
        ...,
        title="Duração Diária",
        description="Duração média de cada sessão diária",
        example=20
    )
    objectives: List[str] = Field(
        ...,
        title="Objetivos",
        description="Objetivos espirituais abordados no plano",
        example=["ansiedade", "paz"]
    )
    bible_experience_level: str = Field(
        ...,
        title="Nível",
        description="Nível de experiência com a Bíblia",
        example="iniciante"
    )
    sessions: List[SessionItem] = Field(
        ...,
        title="Sessões",
        description="Lista de sessões diárias"
    )
