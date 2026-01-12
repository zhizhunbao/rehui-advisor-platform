from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.errors import AppError, AppErrorCode
from src.models.domain import Car
from .dto import CarResponse


class CarService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def search(
        self,
        make: str | None = None,
        model: str | None = None,
        min_year: int | None = None,
        max_year: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        condition: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[CarResponse]:
        query = select(Car)

        if make:
            query = query.where(Car.make == make)
        if model:
            query = query.where(Car.model == model)
        if min_year:
            query = query.where(Car.year >= min_year)
        if max_year:
            query = query.where(Car.year <= max_year)
        if min_price is not None:
            query = query.where(Car.price >= min_price)
        if max_price is not None:
            query = query.where(Car.price <= max_price)
        if condition:
            query = query.where(Car.condition == condition)

        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        cars = list(result.scalars().all())

        return [self._to_response(c) for c in cars]

    async def find_by_id(self, id: str) -> CarResponse:
        result = await self.db.execute(select(Car).where(Car.id == id))
        car = result.scalar_one_or_none()
        if not car:
            raise AppError(AppErrorCode.NOT_FOUND, f"Car {id} not found")
        return self._to_response(car)

    def _to_response(self, car: Car) -> CarResponse:
        return CarResponse(
            id=car.id,
            make=car.make,
            model=car.model,
            year=car.year,
            condition=car.condition,
            mileage=car.mileage,
            price=car.price,
            currency=car.currency,
            color=car.color,
            transmission=car.transmission,
            fuel_type=car.fuel_type,
            features=car.features or [],
        )
