from fastapi import APIRouter, Request

from src.common.logger import log_with_extra
from src.common.response import success_response
from .dto import FrontendLogRequest

router = APIRouter(
    prefix="/logs",
    tags=["logs"],
)


@router.post("/")
def receive_frontend_log(data: FrontendLogRequest, request: Request):
    """接收前端日志并写入后端日志系统"""
    level = data.level.lower()
    if level not in ("debug", "info", "warn", "error"):
        level = "info"

    # 映射 warn -> warning (Python logging 标准)
    log_level = "warning" if level == "warn" else level

    log_with_extra(
        log_level,
        f"[Frontend] {data.message}",
        source="frontend",
        layer=data.layer,
        url=data.url,
        user_agent=data.userAgent,
        frontend_timestamp=data.timestamp,
        error=data.error,
        stack=data.stack,
        caller=data.caller,
        client_ip=request.client.host if request.client else None,
    )

    return success_response(None)
