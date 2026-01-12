from pydantic import BaseModel


class EducationResponse(BaseModel):
    id: str
    institution: str
    program: str
    degree: str
    major: str
    city: str
    state: str | None
    country: str
    tuition: float
    currency: str
    duration: int
    overall_ranking: int | None
    program_ranking: int | None
    admission_rate: float | None
    employment_rate: float | None

    class Config:
        from_attributes = True


class SearchEducationRequest(BaseModel):
    degree: str | None = None
    major: str | None = None
    city: str | None = None
    max_tuition: float | None = None
    page: int = 1
    page_size: int = 20
