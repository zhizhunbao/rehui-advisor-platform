from pydantic import BaseModel
from datetime import datetime

from src.common.enum import AssignmentStatus


class AssignmentCreate(BaseModel):
    lab_id: str
    title: str | None = None  # 默认用 lab 标题
    notebook_file_id: str | None = None  # jupyter notebook 文件 ID
    notes: str | None = None  # 个人笔记


class AssignmentUpdate(BaseModel):
    title: str | None = None
    notebook_file_id: str | None = None
    notes: str | None = None
    status: AssignmentStatus | None = None
    score: float | None = None  # 分数
    feedback: str | None = None  # 老师反馈


class AssignmentResponse(BaseModel):
    id: str
    lab_id: str
    title: str | None
    notebook_file_id: str | None
    notes: str | None
    status: AssignmentStatus
    score: float | None
    feedback: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
