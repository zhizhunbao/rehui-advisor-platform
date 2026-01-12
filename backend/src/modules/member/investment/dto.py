from pydantic import BaseModel


class InvestmentResponse(BaseModel):
    id: str
    product_name: str
    type: str
    ticker: str | None
    current_price: float
    currency: str
    risk_level: str
    minimum_investment: float | None
    provider: str
    description: str | None
    sector: str | None
    dividend_yield: float | None

    class Config:
        from_attributes = True


class SearchInvestmentRequest(BaseModel):
    type: str | None = None
    risk_level: str | None = None
    min_price: float | None = None
    max_price: float | None = None
    page: int = 1
    page_size: int = 20
