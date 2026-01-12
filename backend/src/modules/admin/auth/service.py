"""管理员认证服务 - 使用 Supabase API"""
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from src.common.errors import AppError, AppErrorCode
from src.common.supabase import get_supabase_admin
from src.common.config import get_settings

settings = get_settings()


class AdminAuthService:
    def __init__(self) -> None:
        self.client = get_supabase_admin()
        self.table = "admin_users"

    def login(self, username: str, password: str) -> dict:
        """管理员登录"""
        response = (
            self.client.table(self.table)
            .select("*")
            .or_(f"username.eq.{username},email.eq.{username}")
            .maybe_single()
            .execute()
        )
        admin = response.data

        if not admin:
            raise AppError(AppErrorCode.UNAUTHORIZED, "Invalid credentials")

        if not admin.get("is_active"):
            raise AppError(AppErrorCode.FORBIDDEN, "Account is disabled")

        if not bcrypt.checkpw(password.encode(), admin["password_hash"].encode()):
            raise AppError(AppErrorCode.UNAUTHORIZED, "Invalid credentials")

        # 更新最后登录时间
        self.client.table(self.table).update({
            "last_login_at": datetime.now(timezone.utc).isoformat()
        }).eq("id", admin["id"]).execute()

        return admin

    def get_by_id(self, admin_id: str) -> dict | None:
        """根据 ID 获取管理员"""
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("id", admin_id)
            .maybe_single()
            .execute()
        )
        return response.data

    def create_admin(
        self,
        username: str,
        email: str,
        password: str,
        name: str | None = None,
        role: str = "admin",
    ) -> dict:
        """创建管理员"""
        # 检查用户名或邮箱是否已存在
        existing = (
            self.client.table(self.table)
            .select("id")
            .or_(f"username.eq.{username},email.eq.{email}")
            .maybe_single()
            .execute()
        )
        if existing.data:
            raise AppError(AppErrorCode.DUPLICATE, "Username or email already exists")

        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        response = self.client.table(self.table).insert({
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "name": name,
            "role": role,
            "is_active": True,
        }).execute()

        if not response.data:
            raise AppError(AppErrorCode.INTERNAL_ERROR, "Failed to create admin")
        
        return response.data[0]

    def update_password(
        self, admin_id: str, old_password: str, new_password: str
    ) -> None:
        """更新管理员密码"""
        admin = self.get_by_id(admin_id)
        if not admin:
            raise AppError(AppErrorCode.NOT_FOUND, "Admin not found")

        if not bcrypt.checkpw(old_password.encode(), admin["password_hash"].encode()):
            raise AppError(AppErrorCode.UNAUTHORIZED, "Invalid old password")

        new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        self.client.table(self.table).update({
            "password_hash": new_hash
        }).eq("id", admin_id).execute()

    @staticmethod
    def create_access_token(admin: dict) -> str:
        """创建管理员 JWT token"""
        expire = datetime.now(timezone.utc) + timedelta(hours=24)
        payload = {
            "sub": admin["id"],
            "username": admin["username"],
            "role": admin["role"],
            "type": "admin",
            "exp": expire,
        }
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    @staticmethod
    def create_refresh_token(admin_id: str) -> str:
        """创建管理员刷新 token"""
        expire = datetime.now(timezone.utc) + timedelta(days=7)
        payload = {
            "sub": admin_id,
            "type": "admin_refresh",
            "exp": expire,
        }
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    @staticmethod
    def verify_refresh_token(token: str) -> dict:
        """验证管理员刷新 token"""
        try:
            payload = jwt.decode(
                token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
            )
            if payload.get("type") != "admin_refresh":
                raise AppError(AppErrorCode.UNAUTHORIZED, "Invalid refresh token")
            return payload
        except jwt.ExpiredSignatureError:
            raise AppError(AppErrorCode.UNAUTHORIZED, "Token expired")
        except jwt.InvalidTokenError:
            raise AppError(AppErrorCode.UNAUTHORIZED, "Invalid token")
