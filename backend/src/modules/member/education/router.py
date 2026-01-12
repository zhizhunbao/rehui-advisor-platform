"""教育搜索路由 - 使用 Supabase API"""
from fastapi import APIRouter, Query

from src.common.response import success_response
from .service import EducationService

router = APIRouter(prefix="/education", tags=["education"])


@router.get("/search")
def search_education(
    degree: str | None = None,
    major: str | None = None,
    city: str | None = None,
    max_tuition: float | None = Query(None, alias="maxTuition"),
    page: int = 1,
    page_size: int = Query(20, alias="pageSize"),
):
    service = EducationService()
    items = service.search(
        degree=degree,
        major=major,
        city=city,
        max_tuition=max_tuition,
        page=page,
        page_size=page_size,
    )
    return success_response([e.model_dump() for e in items])


@router.get("/{id}")
def get_education(id: str):
    service = EducationService()
    item = service.find_by_id(id)
    return success_response(item.model_dump() if item else None)
