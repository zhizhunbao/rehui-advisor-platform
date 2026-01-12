from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.errors import AppError, AppErrorCode
from src.models.domain import Education
from .dto import EducationResponse


class EducationService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def search(
        self,
        degree: str | None = None,
        major: str | None = None,
        city: str | None = None,
        max_tuition: float | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[EducationResponse]:
        query = select(Education)

        if degree:
            query = query.where(Education.degree == degree)
        if major:
            query = query.where(Education.major == major)
        if city:
            query = query.where(Education.city == city)
        if max_tuition is not None:
            query = query.where(Education.tuition <= max_tuition)

        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        items = list(result.scalars().all())

        return [self._to_response(e) for e in items]

    async def find_by_id(self, id: str) -> EducationResponse:
        result = await self.db.execute(select(Education).where(Education.id == id))
        item = result.scalar_one_or_none()
        if not item:
            raise AppError(AppErrorCode.NOT_FOUND, f"Education {id} not found")
        return self._to_response(item)

    def _to_response(self, edu: Education) -> EducationResponse:
        return EducationResponse(
            id=edu.id,
            institution=edu.institution,
            program=edu.program,
            degree=edu.degree,
            major=edu.major,
            city=edu.city,
            state=edu.state,
            country=edu.country,
            tuition=edu.tuition,
            currency=edu.currency,
            duration=edu.duration,
            overall_ranking=edu.overall_ranking,
            program_ranking=edu.program_ranking,
            admission_rate=edu.admission_rate,
            employment_rate=edu.employment_rate,
        )
