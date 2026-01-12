from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.common.errors import AppError
from src.common.logger import log_with_extra
from src.common.middleware import RequestContextMiddleware, RequestLoggerMiddleware
from src.common.response import error_response, success_response
from src.common.supabase import get_supabase_admin
from src.common.config import get_settings

# 从统一导出模块导入所有路由
from src.modules import (
    # Admin 模块
    admin_router,
    admin_auth_router,
    crawler_router,
    user_router,
    subscription_router,
    admin_recommendation_router,
    conversation_router,
    config_router,
    data_source_router,
    llm_router,
    log_router,
    prompt_router,
    retrieval_router,
    scheduler_router,
    skill_router,
    # Member 模块
    advisor_router,
    auth_router,
    recommendation_router,
    search_router,
    # Shared 模块
    car_router,
    domain_router,
    education_router,
    flight_router,
    hotel_router,
    house_router,
    insurance_router,
    investment_router,
    job_router,
)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    log_with_extra("info", "Starting North America Advisor System")
    
    # 开发环境：清空执行历史日志
    if settings.env == "development":
        try:
            client = get_supabase_admin()
            client.table("job_executions").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            log_with_extra("info", "[Dev] Cleared job_executions table on startup")
        except Exception as e:
            log_with_extra("warn", f"[Dev] Failed to clear job_executions: {str(e)}")
    
    # 启动调度器
    from src.modules.admin.scheduler.executor import start_scheduler
    try:
        start_scheduler()
    except Exception as e:
        log_with_extra("error", f"Failed to start scheduler: {str(e)}")
    
    yield
    
    # Shutdown
    from src.modules.admin.scheduler.executor import stop_scheduler
    stop_scheduler()
    log_with_extra("info", "Shutting down")


app = FastAPI(
    title="North America Advisor",
    description="北美生活决策顾问系统 - 智能推荐平台",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(RequestLoggerMiddleware)
app.add_middleware(RequestContextMiddleware)


# Exception handler
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "unknown")
    log_with_extra(
        "warn",
        f"[Error] {exc.code.value}: {exc.message}",
        request_id=request_id,
        code=exc.code.value,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.code.value, exc.message, exc.details),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "unknown")
    log_with_extra(
        "error",
        f"[Error] Unhandled: {str(exc)}",
        request_id=request_id,
        error_type=type(exc).__name__,
    )
    message = str(exc) if settings.debug else "Internal server error"
    return JSONResponse(
        status_code=500,
        content=error_response("INTERNAL_ERROR", message),
    )


# Health check
@app.get("/health")
async def health() -> dict[str, Any]:
    # 检查 Supabase 连接
    try:
        client = get_supabase_admin()
        client.table("admin_users").select("id").limit(1).execute()
        db_status = {"status": "connected", "type": "supabase"}
    except Exception as e:
        db_status = {"status": "disconnected", "error": str(e)}

    return {
        "status": "ok",
        "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "environment": settings.env,
        "database": db_status,
    }


# Root
@app.get("/")
async def root():
    return success_response(
        {
            "message": "North America Advisor API",
            "version": "1.0.0",
            "docs": "/docs",
        }
    )


# API info
@app.get(f"{settings.api_prefix}")
async def api_info():
    return success_response(
        {
            "message": "API is ready",
            "version": "1.0.0",
            "endpoints": [
                "GET /health",
                f"POST {settings.api_prefix}/auth/session/anonymous",
                f"POST {settings.api_prefix}/auth/register",
                f"POST {settings.api_prefix}/auth/login",
                f"POST {settings.api_prefix}/auth/refresh",
                f"GET {settings.api_prefix}/auth/me",
                f"PUT {settings.api_prefix}/auth/password",
                f"GET {settings.api_prefix}/auth/quota/status",
                f"POST {settings.api_prefix}/admin/auth/login",
                f"POST {settings.api_prefix}/admin/auth/refresh",
                f"GET {settings.api_prefix}/admin/auth/me",
                f"POST {settings.api_prefix}/advisor/chat",
            ],
        }
    )


# Include routers
# Member 模块
app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(advisor_router, prefix=settings.api_prefix)
app.include_router(search_router, prefix=settings.api_prefix)
app.include_router(recommendation_router, prefix=settings.api_prefix)

# Admin 模块
app.include_router(admin_auth_router, prefix=settings.api_prefix)
app.include_router(admin_router, prefix=settings.api_prefix)
app.include_router(crawler_router, prefix=settings.api_prefix)
app.include_router(user_router, prefix=settings.api_prefix)
app.include_router(subscription_router, prefix=settings.api_prefix)
app.include_router(admin_recommendation_router, prefix=settings.api_prefix)
app.include_router(conversation_router, prefix=settings.api_prefix)
app.include_router(config_router, prefix=settings.api_prefix)
app.include_router(skill_router, prefix=settings.api_prefix)
app.include_router(prompt_router, prefix=settings.api_prefix)
app.include_router(data_source_router, prefix=settings.api_prefix)
app.include_router(log_router, prefix=settings.api_prefix)
app.include_router(llm_router, prefix=settings.api_prefix)
app.include_router(retrieval_router, prefix=settings.api_prefix)
app.include_router(scheduler_router, prefix=settings.api_prefix)

# Shared 模块
app.include_router(domain_router, prefix=settings.api_prefix)
app.include_router(flight_router, prefix=settings.api_prefix)
app.include_router(hotel_router, prefix=settings.api_prefix)
app.include_router(job_router, prefix=settings.api_prefix)
app.include_router(car_router, prefix=settings.api_prefix)
app.include_router(house_router, prefix=settings.api_prefix)
app.include_router(education_router, prefix=settings.api_prefix)
app.include_router(investment_router, prefix=settings.api_prefix)
app.include_router(insurance_router, prefix=settings.api_prefix)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=settings.port, reload=settings.debug)
