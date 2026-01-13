from datetime import datetime
from typing import Any

from pydantic import BaseModel

from src.common.enum import InsuranceType, InsuranceProviderCode


class CoverageDetail(BaseModel):
    type: str
    description: str
    limit: float
    deductible: float
    premium: float


class Discount(BaseModel):
    type: str
    description: str
    amount: float
    percentage: float


class QuoteRequest(BaseModel):
    insurance_type: InsuranceType
    zip_code: str
    user_id: str | None = None
    session_token: str | None = None


class QuoteResponse(BaseModel):
    id: str
    request_id: str
    provider: InsuranceProviderCode
    premium: float
    deductible: float
    coverage_details: list[CoverageDetail]
    discounts: list[Discount]
    total_savings: float
    valid_until: datetime


class ComparisonMetric(BaseModel):
    metric: str
    values: dict[str, float]


class ComparisonResponse(BaseModel):
    quotes: list[QuoteResponse]
    best_value: str
    cheapest: str
    most_coverage: str
    comparison: list[ComparisonMetric]


class RiskFactor(BaseModel):
    factor: str
    impact: str
    weight: float
    description: str


class RiskAssessmentResponse(BaseModel):
    risk_level: str
    factors: list[RiskFactor]
    score: int
    recommendations: list[str]


class ProviderInfo(BaseModel):
    code: str
    name: str
    logo: str | None = None
    rating: float | None = None
    supported_types: list[str]
