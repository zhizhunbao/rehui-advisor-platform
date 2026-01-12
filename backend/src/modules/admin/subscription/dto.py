"""订阅方案管理 DTO"""
from pydantic import BaseModel


class CreateSubscriptionRequest(BaseModel):
    name: str
    name_en: str
    description: str | None = None
    description_en: str | None = None
    price: float
    currency: str = "USD"
    billing_period: str = "monthly"
    daily_quota: int
    features: list[str] = []
    is_active: bool = True
    sort_order: int = 0


class UpdateSubscriptionRequest(BaseModel):
    name: str | None = None
    name_en: str | None = None
    description: str | None = None
    description_en: str | None = None
    price: float | None = None
    currency: str | None = None
    billing_period: str | None = None
    daily_quota: int | None = None
    features: list[str] | None = None
    is_active: bool | None = None
    sort_order: int | None = None
