"""用户认证路由 - 使用 Supabase API"""
from fastapi import APIRouter, Depends, Request

from src.common.auth import get_current_user
from src.common.response import success_response
from .dto import (
    AnonymousSessionResponse,
    LoginRequest,
    QuotaStatusResponse,
    RefreshTokenRequest,
    RegisterRequest,
    UpdatePasswordRequest,
    UserResponse,
)
from .service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/session/anonymous")
def create_anonymous_session(request: Request):
    """创建匿名会话"""
    service = AuthService()
    ip_address = request.client.host if request.client else None
    user = service.create_anonymous_session(ip_address)

    return success_response(
        AnonymousSessionResponse(
            session_token=user.get("session_token", ""),
            user_id=user["id"],
            user_type=user.get("user_type", "ANONYMOUS"),
            search_limit=user.get("search_limit", 5),
            search_count=user.get("search_count", 0),
        ).model_dump()
    )


@router.post("/register")
def register(data: RegisterRequest):
    """用户注册"""
    service = AuthService()
    user = service.register(data.email, data.password, data.name)
    access_token = service.create_access_token(user["id"], user.get("user_type", "REGISTERED"))
    refresh_token = service.create_refresh_token(user["id"])

    return success_response({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": user["id"],
        "user_type": user.get("user_type"),
    })


@router.post("/login")
def login(data: LoginRequest):
    """用户登录"""
    service = AuthService()
    user = service.login(data.email, data.password)
    access_token = service.create_access_token(user["id"], user.get("user_type", "REGISTERED"))
    refresh_token = service.create_refresh_token(user["id"])

    return success_response({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": user["id"],
        "user_type": user.get("user_type"),
    })


@router.post("/refresh")
def refresh_token(data: RefreshTokenRequest):
    """刷新 token"""
    service = AuthService()
    payload = service.verify_refresh_token(data.refresh_token)
    user = service.get_user_by_id(payload["sub"])

    if not user:
        from src.common.errors import AppError, AppErrorCode
        raise AppError(AppErrorCode.UNAUTHORIZED, "User not found")

    access_token = service.create_access_token(user["id"], user.get("user_type", "REGISTERED"))
    new_refresh_token = service.create_refresh_token(user["id"])

    return success_response({
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "user_id": user["id"],
        "user_type": user.get("user_type"),
    })


@router.get("/me")
def get_current_user_info(user: dict = Depends(get_current_user)):
    """获取当前用户信息"""
    return success_response(
        UserResponse(
            id=user["id"],
            email=user.get("email"),
            name=user.get("name"),
            user_type=user.get("user_type", "ANONYMOUS"),
            is_anonymous=user.get("is_anonymous", True),
            search_limit=user.get("search_limit", 5),
            search_count=user.get("search_count", 0),
        ).model_dump()
    )


@router.put("/password")
def update_password(
    data: UpdatePasswordRequest,
    user: dict = Depends(get_current_user),
):
    """更新密码"""
    service = AuthService()
    service.update_password(user["id"], data.old_password, data.new_password)
    return success_response({"message": "Password updated successfully"})


@router.get("/quota/status")
def get_quota_status(request: Request):
    """获取配额状态"""
    service = AuthService()

    auth_header = request.headers.get("authorization", "")
    session_token = request.headers.get("x-session-token", "")

    user = None
    if auth_header.startswith("Bearer "):
        try:
            token = auth_header.replace("Bearer ", "")
            payload = service.verify_token(token)
            user = service.get_user_by_id(payload["sub"])
        except Exception:
            pass
    
    if not user and session_token:
        user = service.get_user_by_session_token(session_token)

    if not user:
        return success_response(
            QuotaStatusResponse(
                user_type="ANONYMOUS",
                search_count=0,
                search_limit=5,
                remaining=5,
            ).model_dump()
        )

    quota = service.get_quota_status(user)
    return success_response(QuotaStatusResponse(**quota).model_dump())
