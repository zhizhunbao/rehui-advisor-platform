from pydantic import BaseModel
from datetime import datetime

from src.common.enum import ResourceType


class ResourceCreate(BaseModel):
    url: str
    title: str
    description: str | None = None
    type: ResourceType = ResourceType.LINK
    course_id: str | None = None  # 关联课程
    lab_id: str | None = None  # 关联 lab
    cached_content: str | None = None  # 抓取的 markdown 内容


class ResourceUpdate(BaseModel):
    url: str | None = None
    title: str | None = None
    description: str | None = None
    type: ResourceType | None = None
    course_id: str | None = None
    lab_id: str | None = None
    cached_content: str | None = None


class ResourceResponse(BaseModel):
    id: str
    url: str
    title: str
    description: str | None
    type: ResourceType
    course_id: str | None
    lab_id: str | None
    cached_content: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
