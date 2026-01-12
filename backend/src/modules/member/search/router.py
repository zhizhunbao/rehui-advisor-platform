"""统一搜索路由 - 使用 Supabase API"""
from fastapi import APIRouter

from src.common.response import success_response
from .dto import UnifiedSearchRequest
from .service import SearchService

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/")
def unified_search(request: UnifiedSearchRequest):
    service = SearchService()
    result = service.search(request)
    return success_response(result.model_dump())
