"""统计分析路由"""
from fastapi import APIRouter, Depends

from src.common.auth import get_current_admin
from src.common.response import success_response
from .service import AnalyticsService

router = APIRouter(prefix="/admin/analytics", tags=["analytics"], dependencies=[Depends(get_current_admin)])


@router.get("/summary")
def get_analytics_summary():
    service = AnalyticsService()
    summary = service.get_summary()
    return success_response(summary)
