"""航班搜索路由 - 使用 Supabase API"""
from fastapi import APIRouter, Query

from src.common.response import success_response
from .service import FlightService

router = APIRouter(prefix="/flights", tags=["flight"])


@router.get("/search")
def search_flights(
    departure_code: str = Query(..., alias="from"),
    arrival_code: str = Query(..., alias="to"),
    departure_date: str = Query(..., alias="departureDate"),
    cabin_class: str | None = Query(None, alias="cabinClass"),
    min_price: float | None = Query(None, alias="minPrice"),
    max_price: float | None = Query(None, alias="maxPrice"),
    page: int = 1,
    page_size: int = Query(20, alias="pageSize"),
):
    service = FlightService()
    flights = service.search(
        departure_code=departure_code,
        arrival_code=arrival_code,
        departure_date=departure_date,
        cabin_class=cabin_class,
        min_price=min_price,
        max_price=max_price,
        page=page,
        page_size=page_size,
    )
    return success_response([f.model_dump() for f in flights])


@router.get("/{id}")
def get_flight(id: str):
    service = FlightService()
    flight = service.find_by_id(id)
    return success_response(flight.model_dump() if flight else None)
