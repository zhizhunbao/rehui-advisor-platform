"""认证依赖 - 使用 Supabase API"""
from fastapi import Depends, Request

from src.common.errors import AppError, AppErrorCode
from src.common.supabase import get_supabase_admin
from src.common.config import get_settings

settings = get_settings()


def _get_auth_service():
    """延迟导入 AuthService 避免循环导入"""
    from src.modules.member.auth.service import AuthService
    return AuthService


def get_user_from_request(request: Request) -> dict | None:
    """从请求中获取用户（支持 JWT 和 Session Token）"""
    auth_header = request.headers.get("authorization", "")
    session_token = request.headers.get("x-session-token", "")
    client = get_supabase_admin()
    AuthService = _get_auth_service()

    # 优先使用 JWT
    if auth_header.startswith("Bearer "):
        try:
            token = auth_header.replace("Bearer ", "")
            payload = AuthService.verify_token(token)
            response = (
                client.table("users")
                .select("*")
                .eq("id", payload["sub"])
                .maybe_single()
                .execute()
            )
            return response.data
        except AppError:
            pass

    # 其次使用 Session Token
    if session_token:
        response = (
            client.table("users")
            .select("*")
            .eq("session_token", session_token)
            .maybe_single()
            .execute()
        )
        return response.data

    return None


def check_quota(request: Request) -> dict:
    """检查用户配额，返回用户对象用于后续递增"""
    user = get_user_from_request(request)

    if not user:
        raise AppError(AppErrorCode.UNAUTHORIZED, "Authentication required")

    search_count = user.get("search_count", 0)
    search_limit = user.get("search_limit", 5)

    if search_count >= search_limit:
        raise AppError(
            AppErrorCode.FORBIDDEN,
            "Search quota exceeded",
            details={
                "search_count": search_count,
                "search_limit": search_limit,
                "user_type": user.get("user_type"),
            },
        )

    return user


def get_current_user(request: Request) -> dict:
    """获取当前登录用户"""
    auth_header = request.headers.get("authorization", "")

    if not auth_header.startswith("Bearer "):
        raise AppError(AppErrorCode.UNAUTHORIZED, "Missing or invalid authorization header")

    token = auth_header.replace("Bearer ", "")
    AuthService = _get_auth_service()
    payload = AuthService.verify_token(token)

    client = get_supabase_admin()
    response = (
        client.table("users")
        .select("*")
        .eq("id", payload["sub"])
        .maybe_single()
        .execute()
    )
    user = response.data

    if not user:
        raise AppError(AppErrorCode.UNAUTHORIZED, "User not found")

    return user


def get_current_user_optional(request: Request) -> dict | None:
    """获取当前用户（可选，未登录返回 None）"""
    auth_header = request.headers.get("authorization", "")

    if not auth_header.startswith("Bearer "):
        return None

    try:
        token = auth_header.replace("Bearer ", "")
        AuthService = _get_auth_service()
        payload = AuthService.verify_token(token)
        client = get_supabase_admin()
        response = (
            client.table("users")
            .select("*")
            .eq("id", payload["sub"])
            .maybe_single()
            .execute()
        )
        return response.data
    except AppError:
        return None


def get_current_admin(request: Request) -> dict:
    """获取当前登录管理员"""
    auth_header = request.headers.get("authorization", "")

    if not auth_header.startswith("Bearer "):
        raise AppError(AppErrorCode.UNAUTHORIZED, "Missing or invalid authorization header")

    token = auth_header.replace("Bearer ", "")
    AuthService = _get_auth_service()
    payload = AuthService.verify_token(token)

    # 检查是否是管理员 token
    if payload.get("type") != "admin":
        raise AppError(AppErrorCode.FORBIDDEN, "Admin access required")

    client = get_supabase_admin()
    response = (
        client.table("admin_users")
        .select("*")
        .eq("id", payload["sub"])
        .maybe_single()
        .execute()
    )
    admin = response.data

    if not admin:
        raise AppError(AppErrorCode.UNAUTHORIZED, "Admin not found")

    if not admin.get("is_active"):
        raise AppError(AppErrorCode.FORBIDDEN, "Admin account is disabled")

    return admin


def require_super_admin(request: Request) -> dict:
    """要求超级管理员权限"""
    admin = get_current_admin(request)

    if admin.get("role") != "super_admin":
        raise AppError(AppErrorCode.FORBIDDEN, "Super admin access required")

    return admin
