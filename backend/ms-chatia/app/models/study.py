from datetime import datetime
from uuid import UUID, uuid4
from typing import List, Optional

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship, Mapped

from app.db.base_class import Base


class StudyPlan(Base):
    """
    Modelo que representa um plano de estudo personalizado.

    O plano é gerado pela IA com base nas preferências do usuário
    e contém uma sequência de seções de estudo estruturadas.

    Attributes:
        id: Identificador único do plano
        user_id: ID do usuário dono do plano
        title: Título inspirador do plano
        description: Descrição detalhada do objetivo
        duration_days: Duração total em dias
        daily_duration: Duração diária em minutos
        created_at: Data de criação
        completed_at: Data de conclusão (opcional)
        sections: Lista de seções do plano
    """

    __tablename__ = "study_plans"

    id = Column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    user_id = Column(
        PGUUID(as_uuid=True),
        nullable=False,
        index=True
    )
    title = Column(String(255), nullable=False)
    description = Column(String(1000))
    duration_days = Column(Integer, nullable=False)
    daily_duration = Column(Integer, nullable=False)
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    completed_at = Column(DateTime)

    # Relacionamentos
    sections: Mapped[List["StudySection"]] = relationship(
        "StudySection",
        back_populates="plan",
        cascade="all, delete-orphan"
    )


class StudySection(Base):
    """
    Modelo que representa uma seção diária do plano.

    Cada seção contém uma sequência de conteúdos como
    versículos, reflexões e exercícios práticos.

    Attributes:
        id: Identificador único da seção
        study_plan_id: ID do plano pai
        title: Título da seção
        position: Ordem na sequência (1-based)
        duration_minutes: Duração estimada
        completed: Se foi concluída
        completed_at: Data de conclusão
        contents: Lista de conteúdos
    """

    __tablename__ = "study_sections"

    id = Column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    study_plan_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("study_plans.id"),
        nullable=False
    )
    title = Column(String(255), nullable=False)
    position = Column(Integer, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime)

    # Relacionamentos
    plan: Mapped["StudyPlan"] = relationship(
        "StudyPlan",
        back_populates="sections"
    )
    contents: Mapped[List["StudyContent"]] = relationship(
        "StudyContent",
        back_populates="section",
        cascade="all, delete-orphan"
    )


class StudyContent(Base):
    """
    Modelo que representa um conteúdo dentro da seção.

    Pode ser um versículo, reflexão, exercício ou áudio,
    organizado em uma sequência lógica de estudo.

    Attributes:
        id: Identificador único do conteúdo
        section_id: ID da seção pai
        content_type: Tipo do conteúdo (texto, áudio)
        content: Conteúdo em si
        position: Ordem na sequência (1-based)
        created_at: Data de criação
    """

    __tablename__ = "study_contents"

    id = Column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    section_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("study_sections.id"),
        nullable=False
    )
    content_type = Column(
        String(50),
        nullable=False,
        comment="Tipo: texto, áudio, etc"
    )
    content = Column(
        String(2000),
        nullable=False,
        comment="Conteúdo ou URL do recurso"
    )
    position = Column(
        Integer,
        nullable=False,
        comment="Ordem na seção"
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    # Relacionamentos
    section: Mapped["StudySection"] = relationship(
        "StudySection",
        back_populates="contents"
    )
