from datetime import datetime, timedelta

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.errors import AppError, AppErrorCode
from src.models.domain import Flight
from .dto import AirportInfo, FlightResponse


class FlightService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def search(
        self,
        departure_code: str,
        arrival_code: str,
        departure_date: str,
        cabin_class: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[FlightResponse]:
        date = datetime.fromisoformat(departure_date.replace("Z", "+00:00"))
        next_day = date + timedelta(days=1)

        query = select(Flight).where(
            and_(
                Flight.departure_code == departure_code,
                Flight.arrival_code == arrival_code,
                Flight.departure_time >= date,
                Flight.departure_time < next_day,
            )
        )

        if cabin_class:
            query = query.where(Flight.cabin_class == cabin_class)
        if min_price is not None:
            query = query.where(Flight.price >= min_price)
        if max_price is not None:
            query = query.where(Flight.price <= max_price)

        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        flights = list(result.scalars().all())

        return [self._to_response(f) for f in flights]

    async def find_by_id(self, id: str) -> FlightResponse:
        result = await self.db.execute(select(Flight).where(Flight.id == id))
        flight = result.scalar_one_or_none()
        if not flight:
            raise AppError(AppErrorCode.NOT_FOUND, f"Flight {id} not found")
        return self._to_response(flight)

    def _to_response(self, flight: Flight) -> FlightResponse:
        return FlightResponse(
            id=flight.id,
            airline=flight.airline,
            flight_number=flight.flight_number,
            departure=AirportInfo(
                code=flight.departure_code,
                name=flight.departure_name,
                city=flight.departure_city,
                time=flight.departure_time.isoformat(),
            ),
            arrival=AirportInfo(
                code=flight.arrival_code,
                name=flight.arrival_name,
                city=flight.arrival_city,
                time=flight.arrival_time.isoformat(),
            ),
            duration=flight.duration,
            stops=flight.stops,
            price=flight.price,
            currency=flight.currency,
            cabin_class=flight.cabin_class,
            available_seats=flight.available_seats,
        )
