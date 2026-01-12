from pydantic import BaseModel


class CarResponse(BaseModel):
    id: str
    make: str
    model: str
    year: int
    condition: str
    mileage: int | None
    price: float
    currency: str
    color: str | None
    transmission: str | None
    fuel_type: str | None
    features: list[str]

    class Config:
        from_attributes = True


class SearchCarRequest(BaseModel):
    make: str | None = None
    model: str | None = None
    min_year: int | None = None
    max_year: int | None = None
    min_price: float | None = None
    max_price: float | None = None
    condition: str | None = None
    page: int = 1
    page_size: int = 20
