"""抓取源管理 DTO"""
from pydantic import BaseModel


class CreateCrawlSourceRequest(BaseModel):
    name: str
    url: str
    domain_id: str
    schedule: str
    config: dict
    is_active: bool


class UpdateCrawlSourceRequest(BaseModel):
    name: str
    url: str
    domain_id: str
    schedule: str
    config: dict
    is_active: bool
