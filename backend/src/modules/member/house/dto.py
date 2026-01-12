from pydantic import BaseModel


class HouseResponse(BaseModel):
    id: str
    listing_type: str
    property_type: str
    city: str
    state: str
    price: float
    currency: str
    bedrooms: int
    bathrooms: float
    square_feet: int | None
    year_built: int | None
    features: list[str]

    class Config:
        from_attributes = True


class SearchHouseRequest(BaseModel):
    city: str | None = None
    listing_type: str | None = None
    min_price: float | None = None
    max_price: float | None = None
    min_bedrooms: int | None = None
    page: int = 1
    page_size: int = 20
