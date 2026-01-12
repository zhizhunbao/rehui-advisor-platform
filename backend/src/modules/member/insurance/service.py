"""保险服务 - 使用 Document Store"""
import random
from datetime import datetime, timedelta, timezone

from src.common.document import DocumentStore
from .dto import (
    ComparisonMetric,
    ComparisonResponse,
    CoverageDetail,
    Discount,
    InsuranceProviderCode,
    InsuranceType,
    ProviderInfo,
    QuoteRequest,
    QuoteResponse,
    RiskAssessmentResponse,
    RiskFactor,
)


DOC_TYPE_QUOTE = "member_insurance_quote"


INSURANCE_PROVIDERS: dict[InsuranceProviderCode, ProviderInfo] = {
    InsuranceProviderCode.GEICO: ProviderInfo(
        code="GEICO", name="GEICO", rating=4.5, supported_types=["AUTO", "HOME", "RENTERS"]
    ),
    InsuranceProviderCode.STATE_FARM: ProviderInfo(
        code="STATE_FARM", name="State Farm", rating=4.3, supported_types=["AUTO", "HOME", "LIFE"]
    ),
    InsuranceProviderCode.PROGRESSIVE: ProviderInfo(
        code="PROGRESSIVE", name="Progressive", rating=4.2, supported_types=["AUTO", "HOME"]
    ),
    InsuranceProviderCode.ALLSTATE: ProviderInfo(
        code="ALLSTATE", name="Allstate", rating=4.1, supported_types=["AUTO", "HOME", "LIFE"]
    ),
    InsuranceProviderCode.FARMERS: ProviderInfo(
        code="FARMERS", name="Farmers", rating=4.0, supported_types=["AUTO", "HOME"]
    ),
    InsuranceProviderCode.USAA: ProviderInfo(
        code="USAA", name="USAA", rating=4.8, supported_types=["AUTO", "HOME", "LIFE", "RENTERS"]
    ),
    InsuranceProviderCode.LIBERTY_MUTUAL: ProviderInfo(
        code="LIBERTY_MUTUAL", name="Liberty Mutual", rating=4.0, supported_types=["AUTO", "HOME"]
    ),
}


class InsuranceService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def get_quotes(self, request: QuoteRequest) -> list[QuoteResponse]:
        providers = self._get_providers_by_type(request.insurance_type)
        quotes = [self._generate_quote(p.code, request) for p in providers]
        self._save_quote_record(request, quotes)
        return quotes

    def _get_providers_by_type(self, insurance_type: InsuranceType) -> list[ProviderInfo]:
        return [
            p for p in INSURANCE_PROVIDERS.values() if insurance_type.value in p.supported_types
        ]

    def _generate_quote(
        self, provider: str, request: QuoteRequest
    ) -> QuoteResponse:
        base_premiums = {
            "GEICO": 800,
            "STATE_FARM": 850,
            "PROGRESSIVE": 780,
            "ALLSTATE": 900,
            "FARMERS": 870,
            "USAA": 720,
            "LIBERTY_MUTUAL": 830,
        }
        type_multipliers = {
            InsuranceType.AUTO: 1.0,
            InsuranceType.HOME: 1.5,
            InsuranceType.HEALTH: 3.0,
            InsuranceType.LIFE: 0.8,
            InsuranceType.RENTERS: 0.3,
        }

        base = base_premiums.get(provider, 800)
        multiplier = type_multipliers.get(request.insurance_type, 1.0)
        variation = 0.9 + random.random() * 0.2
        premium = round(base * multiplier * variation)

        return QuoteResponse(
            id=f"quote_{provider}_{int(datetime.now().timestamp())}",
            request_id=f"req_{int(datetime.now().timestamp())}",
            provider=InsuranceProviderCode(provider),
            premium=premium,
            deductible=500,
            coverage_details=[
                CoverageDetail(
                    type="LIABILITY",
                    description="责任险",
                    limit=100000,
                    deductible=0,
                    premium=200,
                )
            ],
            discounts=[
                Discount(type="MULTI_POLICY", description="多保单折扣", amount=50, percentage=5)
            ],
            total_savings=50,
            valid_until=datetime.now(timezone.utc) + timedelta(days=30),
        )

    def _save_quote_record(
        self, request: QuoteRequest, quotes: list[QuoteResponse]
    ) -> None:
        self.store.create(DOC_TYPE_QUOTE, {
            "user_id": request.user_id,
            "session_token": request.session_token,
            "insurance_type": request.insurance_type.value,
            "request_data": request.model_dump(),
            "zip_code": request.zip_code,
            "quotes": [q.model_dump() for q in quotes],
            "status": "ACTIVE",
            "expires_at": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
        }, owner_id=request.user_id)

    def compare_quotes(self, quotes: list[QuoteResponse]) -> ComparisonResponse:
        sorted_by_premium = sorted(quotes, key=lambda q: q.premium)
        cheapest = sorted_by_premium[0].id if sorted_by_premium else ""

        sorted_by_coverage = sorted(
            quotes, key=lambda q: sum(c.limit for c in q.coverage_details), reverse=True
        )
        most_coverage = sorted_by_coverage[0].id if sorted_by_coverage else ""

        sorted_by_value = sorted(
            quotes,
            key=lambda q: sum(c.limit for c in q.coverage_details) / q.premium,
            reverse=True,
        )
        best_value = sorted_by_value[0].id if sorted_by_value else ""

        return ComparisonResponse(
            quotes=quotes,
            best_value=best_value,
            cheapest=cheapest,
            most_coverage=most_coverage,
            comparison=[
                ComparisonMetric(
                    metric="premium", values={q.id: q.premium for q in quotes}
                ),
                ComparisonMetric(
                    metric="deductible", values={q.id: q.deductible for q in quotes}
                ),
                ComparisonMetric(
                    metric="totalSavings", values={q.id: q.total_savings for q in quotes}
                ),
            ],
        )

    def assess_risk(self, request: QuoteRequest) -> RiskAssessmentResponse:
        return RiskAssessmentResponse(
            risk_level="MEDIUM",
            factors=[
                RiskFactor(
                    factor="地理位置",
                    impact="NEUTRAL",
                    weight=0.2,
                    description="您所在地区的风险水平适中",
                )
            ],
            score=65,
            recommendations=["考虑增加责任险保额", "安装安全设备可获得折扣"],
        )

    def get_providers(
        self, insurance_type: InsuranceType | None = None
    ) -> list[ProviderInfo]:
        if insurance_type:
            return self._get_providers_by_type(insurance_type)
        return list(INSURANCE_PROVIDERS.values())
