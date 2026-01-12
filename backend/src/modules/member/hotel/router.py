"""酒店搜索路由 - 使用 Supabase API"""
from fastapi import APIRouter, Query

from src.common.response import success_response
from .service import HotelService

router = APIRouter(prefix="/hotels", tags=["hotel"])


@router.get("/search")
def search_hotels(
    city: str,
    min_price: float | None = Query(None, alias="minPrice"),
    max_price: float | None = Query(None, alias="maxPrice"),
    min_rating: float | None = Query(None, alias="minRating"),
    page: int = 1,
    page_size: int = Query(20, alias="pageSize"),
):
    service = HotelService()
    hotels = service.search(
        city=city,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        page=page,
        page_size=page_size,
    )
    return success_response([h.model_dump() for h in hotels])


@router.get("/{id}")
def get_hotel(id: str):
    service = HotelService()
    hotel = service.find_by_id(id)
    return success_response(hotel.model_dump() if hotel else None)
