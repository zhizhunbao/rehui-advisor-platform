"""投资搜索路由 - 使用 Supabase API"""
from fastapi import APIRouter, Query

from src.common.response import success_response
from .service import InvestmentService

router = APIRouter(prefix="/investments", tags=["investment"])


@router.get("/search")
def search_investments(
    investment_type: str | None = Query(None, alias="type"),
    risk_level: str | None = Query(None, alias="riskLevel"),
    min_price: float | None = Query(None, alias="minPrice"),
    max_price: float | None = Query(None, alias="maxPrice"),
    page: int = 1,
    page_size: int = Query(20, alias="pageSize"),
):
    service = InvestmentService()
    items = service.search(
        investment_type=investment_type,
        risk_level=risk_level,
        min_price=min_price,
        max_price=max_price,
        page=page,
        page_size=page_size,
    )
    return success_response([i.model_dump() for i in items])


@router.get("/{id}")
def get_investment(id: str):
    service = InvestmentService()
    item = service.find_by_id(id)
    return success_response(item.model_dump() if item else None)
