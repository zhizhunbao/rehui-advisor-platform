from pydantic import BaseModel


class JobResponse(BaseModel):
    id: str
    title: str
    company: str
    city: str
    state: str | None
    job_type: str
    salary_min: float | None
    salary_max: float | None
    currency: str
    description: str
    requirements: list[str]
    benefits: list[str]

    class Config:
        from_attributes = True


class SearchJobRequest(BaseModel):
    city: str | None = None
    job_type: str | None = None
    min_salary: float | None = None
    keyword: str | None = None
    page: int = 1
    page_size: int = 20
