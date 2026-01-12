from pydantic import BaseModel


class HotelResponse(BaseModel):
    id: str
    name: str
    city: str
    state: str | None
    country: str
    rating: float | None
    review_score: float | None
    price_per_night: float
    currency: str
    amenities: list[str]

    class Config:
        from_attributes = True


class SearchHotelRequest(BaseModel):
    city: str
    check_in: str
    check_out: str
    guests: int = 1
    min_price: float | None = None
    max_price: float | None = None
    min_rating: float | None = None
    page: int = 1
    page_size: int = 20
