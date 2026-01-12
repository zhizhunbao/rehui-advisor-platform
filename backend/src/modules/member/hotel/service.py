from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.errors import AppError, AppErrorCode
from src.models.domain import Hotel
from .dto import HotelResponse


class HotelService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def search(
        self,
        city: str,
        min_price: float | None = None,
        max_price: float | None = None,
        min_rating: float | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[HotelResponse]:
        query = select(Hotel).where(Hotel.city == city)

        if min_price is not None:
            query = query.where(Hotel.price_per_night >= min_price)
        if max_price is not None:
            query = query.where(Hotel.price_per_night <= max_price)
        if min_rating is not None:
            query = query.where(Hotel.review_score >= min_rating)

        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        hotels = list(result.scalars().all())

        return [self._to_response(h) for h in hotels]

    async def find_by_id(self, id: str) -> HotelResponse:
        result = await self.db.execute(select(Hotel).where(Hotel.id == id))
        hotel = result.scalar_one_or_none()
        if not hotel:
            raise AppError(AppErrorCode.NOT_FOUND, f"Hotel {id} not found")
        return self._to_response(hotel)

    def _to_response(self, hotel: Hotel) -> HotelResponse:
        return HotelResponse(
            id=hotel.id,
            name=hotel.name,
            city=hotel.city,
            state=hotel.state,
            country=hotel.country,
            rating=hotel.rating,
            review_score=hotel.review_score,
            price_per_night=hotel.price_per_night,
            currency=hotel.currency,
            amenities=hotel.amenities or [],
        )
