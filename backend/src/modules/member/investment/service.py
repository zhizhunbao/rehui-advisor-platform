from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.errors import AppError, AppErrorCode
from src.models.domain import Investment
from .dto import InvestmentResponse


class InvestmentService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def search(
        self,
        investment_type: str | None = None,
        risk_level: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[InvestmentResponse]:
        query = select(Investment)

        if investment_type:
            query = query.where(Investment.type == investment_type)
        if risk_level:
            query = query.where(Investment.risk_level == risk_level)
        if min_price is not None:
            query = query.where(Investment.current_price >= min_price)
        if max_price is not None:
            query = query.where(Investment.current_price <= max_price)

        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        items = list(result.scalars().all())

        return [self._to_response(i) for i in items]

    async def find_by_id(self, id: str) -> InvestmentResponse:
        result = await self.db.execute(select(Investment).where(Investment.id == id))
        item = result.scalar_one_or_none()
        if not item:
            raise AppError(AppErrorCode.NOT_FOUND, f"Investment {id} not found")
        return self._to_response(item)

    def _to_response(self, inv: Investment) -> InvestmentResponse:
        return InvestmentResponse(
            id=inv.id,
            product_name=inv.product_name,
            type=inv.type,
            ticker=inv.ticker,
            current_price=inv.current_price,
            currency=inv.currency,
            risk_level=inv.risk_level,
            minimum_investment=inv.minimum_investment,
            provider=inv.provider,
            description=inv.description,
            sector=inv.sector,
            dividend_yield=inv.dividend_yield,
        )
