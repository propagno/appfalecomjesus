from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class UserPreferences(BaseModel):
    user_id: str
    name: Optional[str] = ""
    email: Optional[str] = ""
    objectives: List[str]
    bible_experience_level: str
    content_preferences: List[str]
    preferred_time: str
    onboarding_completed: Optional[bool] = False
    has_study_plan: Optional[bool] = False


class UserPreferencesResponse(UserPreferences):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StudyContentBase(BaseModel):
    content_type: str
    content: str
    reference: Optional[str] = None
    position: int


class StudyContentCreate(StudyContentBase):
    pass


class StudyContentResponse(StudyContentBase):
    id: str
    section_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class StudySectionBase(BaseModel):
    title: str
    description: Optional[str] = None
    day_number: int
    position: int
    duration_minutes: int = 15


class StudySectionCreate(StudySectionBase):
    pass


class StudySectionResponse(StudySectionBase):
    id: str
    study_plan_id: str
    created_at: datetime
    contents: Optional[List[StudyContentResponse]] = None

    class Config:
        from_attributes = True


class StudyPlanBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration_days: int


class StudyPlanCreate(StudyPlanBase):
    user_id: str


class StudyPlanResponse(StudyPlanBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    sections: Optional[List[StudySectionResponse]] = None

    class Config:
        from_attributes = True


class UserStudyProgressBase(BaseModel):
    completed: bool = False
    user_notes: Optional[str] = None


class UserStudyProgressCreate(UserStudyProgressBase):
    section_id: str


class UserStudyProgressUpdate(UserStudyProgressBase):
    pass


class UserStudyProgressResponse(UserStudyProgressBase):
    id: str
    user_id: str
    section_id: str
    completion_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserReflectionBase(BaseModel):
    content: str


class UserReflectionCreate(UserReflectionBase):
    section_id: str


class UserReflectionResponse(UserReflectionBase):
    id: str
    user_id: str
    section_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DailyDevotionalResponse(BaseModel):
    id: str
    title: str
    verse: str
    reference: str
    reflection: str
    created_at: datetime

    class Config:
        from_attributes = True
