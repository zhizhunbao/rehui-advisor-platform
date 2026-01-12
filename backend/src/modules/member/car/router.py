"""汽车搜索路由 - 使用 Supabase API"""
from fastapi import APIRouter, Query

from src.common.response import success_response
from .service import CarService

router = APIRouter(prefix="/cars", tags=["car"])


@router.get("/search")
def search_cars(
    make: str | None = None,
    model: str | None = None,
    min_year: int | None = Query(None, alias="minYear"),
    max_year: int | None = Query(None, alias="maxYear"),
    min_price: float | None = Query(None, alias="minPrice"),
    max_price: float | None = Query(None, alias="maxPrice"),
    condition: str | None = None,
    page: int = 1,
    page_size: int = Query(20, alias="pageSize"),
):
    service = CarService()
    cars = service.search(
        make=make,
        model=model,
        min_year=min_year,
        max_year=max_year,
        min_price=min_price,
        max_price=max_price,
        condition=condition,
        page=page,
        page_size=page_size,
    )
    return success_response([c.model_dump() for c in cars])


@router.get("/{id}")
def get_car(id: str):
    service = CarService()
    car = service.find_by_id(id)
    return success_response(car.model_dump() if car else None)
