"""房产搜索路由 - 使用 Supabase API"""
from fastapi import APIRouter, Query

from src.common.response import success_response
from .service import HouseService

router = APIRouter(prefix="/houses", tags=["house"])


@router.get("/search")
def search_houses(
    city: str | None = None,
    listing_type: str | None = Query(None, alias="listingType"),
    min_price: float | None = Query(None, alias="minPrice"),
    max_price: float | None = Query(None, alias="maxPrice"),
    min_bedrooms: int | None = Query(None, alias="minBedrooms"),
    page: int = 1,
    page_size: int = Query(20, alias="pageSize"),
):
    service = HouseService()
    houses = service.search(
        city=city,
        listing_type=listing_type,
        min_price=min_price,
        max_price=max_price,
        min_bedrooms=min_bedrooms,
        page=page,
        page_size=page_size,
    )
    return success_response([h.model_dump() for h in houses])


@router.get("/{id}")
def get_house(id: str):
    service = HouseService()
    house = service.find_by_id(id)
    return success_response(house.model_dump() if house else None)
