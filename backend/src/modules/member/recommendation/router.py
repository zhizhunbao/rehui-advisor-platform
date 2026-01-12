"""推荐服务路由 - 使用 Supabase API"""
from fastapi import APIRouter

from src.common.response import success_response
from .dto import RecommendationRequest
from .service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["recommendation"])


@router.post("/")
def get_recommendations(request: RecommendationRequest):
    service = RecommendationService()
    result = service.get_recommendations(request)
    return success_response(result.model_dump())
