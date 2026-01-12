"""用户管理路由"""
from fastapi import APIRouter, Depends

from src.common.auth import get_current_admin
from src.common.response import success_response
from .service import UserAdminService

router = APIRouter(
    prefix="/admin/users",
    tags=["admin-users"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("/")
def get_users(
    page: int = 1,
    limit: int = 20,
    search: str | None = None,
    status: str | None = None,
    subscription_plan: str | None = None,
):
    service = UserAdminService()
    users, total = service.find_all(page, limit, search, status, subscription_plan)
    return success_response(users, meta={"total": total, "page": page, "limit": limit})


@router.get("/stats")
def get_user_stats():
    service = UserAdminService()
    stats = service.get_user_stats()
    return success_response(stats)


@router.get("/{id}")
def get_user(id: str):
    service = UserAdminService()
    user = service.find_by_id(id)
    return success_response(user)


@router.put("/{id}")
def update_user(id: str, data: dict):
    service = UserAdminService()
    user = service.update(id, data)
    return success_response(user)


@router.post("/{id}/toggle-status")
def toggle_user_status(id: str):
    service = UserAdminService()
    user = service.toggle_status(id)
    return success_response(user)


@router.put("/{id}/subscription")
def update_user_subscription(id: str, plan: str):
    service = UserAdminService()
    user = service.update_subscription(id, plan)
    return success_response(user)
