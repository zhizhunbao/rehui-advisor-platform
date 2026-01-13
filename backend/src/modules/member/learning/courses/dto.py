from pydantic import BaseModel
from datetime import datetime


class CourseCreate(BaseModel):
    name: str  # e.g., "Reinforcement Learning"
    code: str | None = None  # e.g., "CS234"
    description: str | None = None
    semester: str | None = None  # e.g., "2026 Spring"
    instructor: str | None = None


class CourseUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    description: str | None = None
    semester: str | None = None
    instructor: str | None = None


class CourseResponse(BaseModel):
    id: str
    name: str
    code: str | None
    description: str | None
    semester: str | None
    instructor: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
