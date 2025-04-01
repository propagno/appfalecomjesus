import uuid
from sqlalchemy import Column, String, DateTime, Boolean, JSON, ForeignKey, Integer, Text
from sqlalchemy.sql import func
from app.infrastructure.database import Base


class UserPreferences(Base):
    __tablename__ = "user_preferences"
    __table_args__ = {"schema": "study_schema"}

    id = Column(String, primary_key=True, index=True,
                default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True, unique=True)
    objectives = Column(JSON, nullable=False)
    bible_experience_level = Column(String, nullable=False)
    content_preferences = Column(JSON, nullable=False)
    preferred_time = Column(String, nullable=False)
    onboarding_completed = Column(Boolean, default=False)
    has_study_plan = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<UserPreferences for user {self.user_id}>"


class StudyPlan(Base):
    __tablename__ = "study_plans"
    __table_args__ = {"schema": "study_schema"}

    id = Column(String, primary_key=True, index=True,
                default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    duration_days = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<StudyPlan {self.title} for user {self.user_id}>"


class StudySection(Base):
    __tablename__ = "study_sections"
    __table_args__ = {"schema": "study_schema"}

    id = Column(String, primary_key=True, index=True,
                default=lambda: str(uuid.uuid4()))
    study_plan_id = Column(String, ForeignKey(
        "study_schema.study_plans.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    day_number = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False)
    duration_minutes = Column(Integer, nullable=False, default=15)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<StudySection {self.title} for plan {self.study_plan_id}>"


class StudyContent(Base):
    __tablename__ = "study_contents"
    __table_args__ = {"schema": "study_schema"}

    id = Column(String, primary_key=True, index=True,
                default=lambda: str(uuid.uuid4()))
    section_id = Column(String, ForeignKey(
        "study_schema.study_sections.id"), nullable=False)
    # "verse", "reflection", "prayer", etc.
    content_type = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    reference = Column(String)  # Bible reference for verses
    position = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<StudyContent {self.content_type} for section {self.section_id}>"


class UserStudyProgress(Base):
    __tablename__ = "user_study_progress"
    __table_args__ = {"schema": "study_schema"}

    id = Column(String, primary_key=True, index=True,
                default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    section_id = Column(String, ForeignKey(
        "study_schema.study_sections.id"), nullable=False)
    completed = Column(Boolean, default=False)
    completion_date = Column(DateTime(timezone=True))
    user_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<UserStudyProgress for user {self.user_id}, section {self.section_id}>"


class UserReflection(Base):
    __tablename__ = "user_reflections"
    __table_args__ = {"schema": "study_schema"}

    id = Column(String, primary_key=True, index=True,
                default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    section_id = Column(String, ForeignKey(
        "study_schema.study_sections.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<UserReflection for user {self.user_id}, section {self.section_id}>"
