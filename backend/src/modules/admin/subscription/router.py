"""订阅方案管理路由"""
from fastapi import APIRouter, Depends

from src.common.auth import get_current_admin
from src.common.response import success_response
from .dto import CreateSubscriptionRequest, UpdateSubscriptionRequest
from .service import SubscriptionService

router = APIRouter(
    prefix="/admin/subscriptions",
    tags=["admin-subscriptions"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("/")
def get_subscriptions(
    page: int = 1,
    limit: int = 20,
    is_active: bool | None = None,
):
    service = SubscriptionService()
    plans, total = service.find_all(page, limit, is_active)
    return success_response(plans, meta={"total": total, "page": page, "limit": limit})


@router.get("/active")
def get_active_subscriptions():
    """获取所有激活的订阅方案（公开接口）"""
    service = SubscriptionService()
    plans = service.find_active()
    return success_response(plans)


@router.get("/{id}")
def get_subscription(id: str):
    service = SubscriptionService()
    plan = service.find_by_id(id)
    return success_response(plan)


@router.post("/")
def create_subscription(data: CreateSubscriptionRequest):
    service = SubscriptionService()
    plan = service.create(data.model_dump())
    return success_response(plan)


@router.put("/{id}")
def update_subscription(id: str, data: UpdateSubscriptionRequest):
    service = SubscriptionService()
    plan = service.update(id, data.model_dump(exclude_unset=True))
    return success_response(plan)


@router.delete("/{id}")
def delete_subscription(id: str):
    service = SubscriptionService()
    service.delete(id)
    return success_response(None)


@router.post("/{id}/toggle")
def toggle_subscription(id: str):
    service = SubscriptionService()
    plan = service.toggle_status(id)
    return success_response(plan)
