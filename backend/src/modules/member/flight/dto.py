from datetime import datetime

from pydantic import BaseModel


class AirportInfo(BaseModel):
    code: str
    name: str
    city: str
    time: str


class FlightResponse(BaseModel):
    id: str
    airline: str
    flight_number: str
    departure: AirportInfo
    arrival: AirportInfo
    duration: int
    stops: int
    price: float
    currency: str
    cabin_class: str
    available_seats: int | None = None

    class Config:
        from_attributes = True


class SearchFlightRequest(BaseModel):
    departure_code: str
    arrival_code: str
    departure_date: str
    return_date: str | None = None
    passengers: int = 1
    cabin_class: str | None = None
    min_price: float | None = None
    max_price: float | None = None
    page: int = 1
    page_size: int = 20
