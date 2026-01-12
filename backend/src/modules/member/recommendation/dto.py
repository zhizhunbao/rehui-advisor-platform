from pydantic import BaseModel


class RecommendationItem(BaseModel):
    id: str
    domain: str
    item_id: str
    match_score: float
    ranking: int
    pros: list[str]
    cons: list[str]
    reasoning: str


class RecommendationRequest(BaseModel):
    user_id: str
    domain: str
    preferences: dict
    limit: int


class RecommendationResponse(BaseModel):
    items: list[RecommendationItem]
    total: int
