from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.errors import AppError, AppErrorCode
from src.models.domain import House
from .dto import HouseResponse


class HouseService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def search(
        self,
        city: str | None = None,
        listing_type: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        min_bedrooms: int | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[HouseResponse]:
        query = select(House)

        if city:
            query = query.where(House.city == city)
        if listing_type:
            query = query.where(House.listing_type == listing_type)
        if min_price is not None:
            query = query.where(House.price >= min_price)
        if max_price is not None:
            query = query.where(House.price <= max_price)
        if min_bedrooms is not None:
            query = query.where(House.bedrooms >= min_bedrooms)

        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        houses = list(result.scalars().all())

        return [self._to_response(h) for h in houses]

    async def find_by_id(self, id: str) -> HouseResponse:
        result = await self.db.execute(select(House).where(House.id == id))
        house = result.scalar_one_or_none()
        if not house:
            raise AppError(AppErrorCode.NOT_FOUND, f"House {id} not found")
        return self._to_response(house)

    def _to_response(self, house: House) -> HouseResponse:
        return HouseResponse(
            id=house.id,
            listing_type=house.listing_type,
            property_type=house.property_type,
            city=house.city,
            state=house.state,
            price=house.price,
            currency=house.currency,
            bedrooms=house.bedrooms,
            bathrooms=house.bathrooms,
            square_feet=house.square_feet,
            year_built=house.year_built,
            features=house.features or [],
        )
