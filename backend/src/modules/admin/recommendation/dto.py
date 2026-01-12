"""推荐方案管理 DTO"""
from pydantic import BaseModel


class UpdateRecommendationRequest(BaseModel):
    match_score: float | None = None
    ranking: int | None = None
    pros: list[str] | None = None
    cons: list[str] | None = None
    reasoning: str | None = None
