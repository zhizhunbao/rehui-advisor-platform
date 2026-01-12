"""Analytics DTO"""
from pydantic import BaseModel


class AnalyticsSummaryResponse(BaseModel):
    total_users: int
    total_sessions: int
    total_messages: int
    active_users_today: int
    popular_domains: list[dict]
    recent_activity: list[dict]
