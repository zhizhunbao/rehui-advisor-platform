"""推荐方案管理路由"""
from fastapi import APIRouter, Depends

from src.common.auth import get_current_admin
from src.common.response import success_response
from .dto import UpdateRecommendationRequest
from .service import RecommendationAdminService

router = APIRouter(
    prefix="/admin/recommendations",
    tags=["admin-recommendations"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("/")
def get_recommendations(
    page: int = 1,
    limit: int = 20,
    user_id: str | None = None,
    domain: str | None = None,
):
    service = RecommendationAdminService()
    recommendations, total = service.find_all(page, limit, user_id, domain)
    return success_response(recommendations, meta={"total": total, "page": page, "limit": limit})


@router.get("/stats")
def get_recommendation_stats():
    service = RecommendationAdminService()
    stats = service.get_stats()
    return success_response(stats)


@router.get("/{id}")
def get_recommendation(id: str):
    service = RecommendationAdminService()
    recommendation = service.find_by_id(id)
    return success_response(recommendation)


@router.get("/user/{user_id}")
def get_user_recommendations(user_id: str, domain: str | None = None):
    service = RecommendationAdminService()
    recommendations = service.find_by_user(user_id, domain)
    return success_response(recommendations)


@router.put("/{id}")
def update_recommendation(id: str, data: UpdateRecommendationRequest):
    service = RecommendationAdminService()
    recommendation = service.update(id, data.model_dump(exclude_unset=True))
    return success_response(recommendation)


@router.delete("/{id}")
def delete_recommendation(id: str):
    service = RecommendationAdminService()
    service.delete(id)
    return success_response(None)


@router.delete("/user/{user_id}")
def delete_user_recommendations(user_id: str):
    service = RecommendationAdminService()
    count = service.delete_by_user(user_id)
    return success_response({"deleted": count})
