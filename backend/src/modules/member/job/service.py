from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.errors import AppError, AppErrorCode
from src.models.domain import Job
from .dto import JobResponse


class JobService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def search(
        self,
        city: str | None = None,
        job_type: str | None = None,
        min_salary: float | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[JobResponse]:
        query = select(Job)

        if city:
            query = query.where(Job.city == city)
        if job_type:
            query = query.where(Job.job_type == job_type)
        if min_salary is not None:
            query = query.where(Job.salary_min >= min_salary)

        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        jobs = list(result.scalars().all())

        return [self._to_response(j) for j in jobs]

    async def find_by_id(self, id: str) -> JobResponse:
        result = await self.db.execute(select(Job).where(Job.id == id))
        job = result.scalar_one_or_none()
        if not job:
            raise AppError(AppErrorCode.NOT_FOUND, f"Job {id} not found")
        return self._to_response(job)

    def _to_response(self, job: Job) -> JobResponse:
        return JobResponse(
            id=job.id,
            title=job.title,
            company=job.company,
            city=job.city,
            state=job.state,
            job_type=job.job_type,
            salary_min=job.salary_min,
            salary_max=job.salary_max,
            currency=job.currency,
            description=job.description,
            requirements=job.requirements or [],
            benefits=job.benefits or [],
        )
