import time
import uuid
from typing import Any, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.common.errors import AppError
from src.common.logger import log_with_extra
from src.common.config import get_settings

settings = get_settings()

SENSITIVE_FIELDS = {"password", "token", "secret", "api_key", "authorization"}


def sanitize_dict(data: dict[str, Any]) -> dict[str, Any]:
    return {k: "***" if k.lower() in SENSITIVE_FIELDS else v for k, v in data.items()}


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        start_time = time.time()

        request.state.request_id = request_id
        request.state.start_time = start_time

        response = await call_next(request)
        response.headers["X-Request-Id"] = request_id

        return response


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = getattr(request.state, "request_id", "unknown")
        start_time = getattr(request.state, "start_time", time.time())

        # Log request
        log_with_extra(
            "info",
            f"[HTTP] --> {request.method} {request.url.path}",
            request_id=request_id,
            query=dict(request.query_params),
            ip=request.client.host if request.client else None,
        )

        response = await call_next(request)

        # Log response
        duration = int((time.time() - start_time) * 1000)
        level = "warn" if response.status_code >= 400 else "info"
        log_with_extra(
            level,
            f"[HTTP] <-- {request.method} {request.url.path} {response.status_code} {duration}ms",
            request_id=request_id,
            status_code=response.status_code,
            duration=duration,
        )

        return response


def create_error_response(error: AppError, request_id: str) -> dict[str, Any]:
    log_with_extra(
        "warn",
        f"[Error] {error.code.value}: {error.message}",
        request_id=request_id,
        code=error.code.value,
        details=error.details,
    )
    return {"success": False, "error": error.to_dict()}
