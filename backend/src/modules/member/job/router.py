"""工作搜索路由 - 使用 Supabase API"""
from fastapi import APIRouter, Query

from src.common.response import success_response
from .service import JobService

router = APIRouter(prefix="/jobs", tags=["job"])


@router.get("/search")
def search_jobs(
    city: str | None = None,
    job_type: str | None = Query(None, alias="jobType"),
    min_salary: float | None = Query(None, alias="minSalary"),
    page: int = 1,
    page_size: int = Query(20, alias="pageSize"),
):
    service = JobService()
    jobs = service.search(
        city=city,
        job_type=job_type,
        min_salary=min_salary,
        page=page,
        page_size=page_size,
    )
    return success_response([j.model_dump() for j in jobs])


@router.get("/{id}")
def get_job(id: str):
    service = JobService()
    job = service.find_by_id(id)
    return success_response(job.model_dump() if job else None)
