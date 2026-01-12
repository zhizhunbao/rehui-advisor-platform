"""管理员认证路由 - 使用 Supabase API"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.common.auth import get_current_admin
from src.common.response import success_response
from .dto import (
    AdminLoginRequest,
    AdminResponse,
    CreateAdminRequest,
    UpdateAdminPasswordRequest,
)
from .service import AdminAuthService

router = APIRouter(prefix="/admin/auth", tags=["admin-auth"])


class RefreshTokenRequest(BaseModel):
    refresh_token: str


@router.post("/login")
def admin_login(data: AdminLoginRequest):
    """管理员登录"""
    service = AdminAuthService()
    admin = service.login(data.username, data.password)
    access_token = AdminAuthService.create_access_token(admin)
    refresh_token = AdminAuthService.create_refresh_token(admin["id"])

    return success_response({
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "tokenType": "bearer",
        "admin": {
            "id": admin["id"],
            "username": admin["username"],
            "email": admin["email"],
            "name": admin.get("name"),
            "role": admin["role"],
        },
    })


@router.post("/refresh")
def refresh_token(data: RefreshTokenRequest):
    """刷新管理员 token"""
    service = AdminAuthService()
    payload = service.verify_refresh_token(data.refresh_token)
    admin = service.get_by_id(payload["sub"])

    if not admin:
        from src.common.errors import AppError, AppErrorCode
        raise AppError(AppErrorCode.UNAUTHORIZED, "Admin not found")

    if not admin.get("is_active"):
        from src.common.errors import AppError, AppErrorCode
        raise AppError(AppErrorCode.FORBIDDEN, "Admin account is disabled")

    access_token = AdminAuthService.create_access_token(admin)
    new_refresh_token = AdminAuthService.create_refresh_token(admin["id"])

    return success_response({
        "accessToken": access_token,
        "refreshToken": new_refresh_token,
        "tokenType": "bearer",
    })


@router.get("/me")
def get_current_admin_info(admin: dict = Depends(get_current_admin)):
    """获取当前管理员信息"""
    return success_response({
        "id": admin["id"],
        "username": admin["username"],
        "email": admin["email"],
        "name": admin.get("name"),
        "role": admin["role"],
        "isActive": admin.get("is_active", True),
        "lastLoginAt": admin.get("last_login_at"),
    })


@router.put("/password")
def update_admin_password(
    data: UpdateAdminPasswordRequest,
    admin: dict = Depends(get_current_admin),
):
    """更新管理员密码"""
    service = AdminAuthService()
    service.update_password(admin["id"], data.old_password, data.new_password)
    return success_response({"message": "Password updated successfully"})


@router.post("/create")
def create_admin(
    data: CreateAdminRequest,
    current_admin: dict = Depends(get_current_admin),
):
    """创建新管理员（仅超级管理员可用）"""
    from src.common.errors import AppError, AppErrorCode

    if current_admin.get("role") != "super_admin":
        raise AppError(AppErrorCode.FORBIDDEN, "Only super admin can create new admins")

    service = AdminAuthService()
    admin = service.create_admin(
        username=data.username,
        email=data.email,
        password=data.password,
        name=data.name,
        role=data.role,
    )

    return success_response({
        "id": admin["id"],
        "username": admin["username"],
        "email": admin["email"],
        "name": admin.get("name"),
        "role": admin["role"],
        "isActive": admin.get("is_active", True),
        "lastLoginAt": None,
    })
