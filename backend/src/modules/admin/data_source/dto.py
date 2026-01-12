"""Data Source DTOs"""
from pydantic import BaseModel


class CreateDataSourceRequest(BaseModel):
    url: str
    name: str
    description: str
    type: str
    category_id: str
    domain_id: str
    tags: list[str]
    notes: str
    config: dict


class UpdateDataSourceRequest(BaseModel):
    name: str
    description: str
    type: str
    category_id: str
    domain_id: str
    tags: list[str]
    status: str
    is_featured: bool
    quality_score: int
    notes: str
    config: dict


class BatchAddRequest(BaseModel):
    urls: list[str]
    type: str
    category_id: str


class GitHubDiscoverRequest(BaseModel):
    query: str
    sort: str  # stars, updated, forks
    order: str  # desc, asc
    per_page: int
    category_id: str
    domain_id: str


class GitHubDiscoverResult(BaseModel):
    url: str
    name: str
    full_name: str
    description: str
    stars: int
    forks: int
    language: str
    topics: list[str]
    updated_at: str
    owner: str
    repo: str


class BatchImportRequest(BaseModel):
    items: list[dict]
    category_id: str
    domain_id: str | None
