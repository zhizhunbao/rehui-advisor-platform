from typing import Any

from pydantic import BaseModel


class UnifiedSearchRequest(BaseModel):
    domain: str
    query: str
    filters: dict[str, Any] | None = None
    page: int = 1
    page_size: int = 20


class SearchResultItem(BaseModel):
    id: str
    domain: str
    title: str
    description: str | None
    price: float | None
    currency: str | None
    score: float
    data: dict[str, Any]


class SearchResponse(BaseModel):
    items: list[SearchResultItem]
    total: int
    page: int
    page_size: int
