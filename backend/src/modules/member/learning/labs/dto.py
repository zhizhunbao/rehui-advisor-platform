from pydantic import BaseModel
from datetime import datetime


class LabCreate(BaseModel):
    course_id: str
    title: str  # e.g., "Lab 1: Q-Learning Implementation"
    description: str | None = None
    instructions_md: str | None = None  # 转换后的 markdown 内容
    original_file_id: str | None = None  # 原始 docx/pdf 文件 ID
    due_date: datetime | None = None
    order: int = 0  # 排序


class LabUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    instructions_md: str | None = None
    original_file_id: str | None = None
    due_date: datetime | None = None
    order: int | None = None


class LabResponse(BaseModel):
    id: str
    course_id: str
    title: str
    description: str | None
    instructions_md: str | None
    original_file_id: str | None
    due_date: datetime | None
    order: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
