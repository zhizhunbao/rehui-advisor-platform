"""用户认证服务 - 使用 Supabase API"""
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from src.common.errors import AppError, AppErrorCode
from src.common.supabase import get_supabase_admin
from src.common.config import get_settings

settings = get_settings()


class AuthService:
    def __init__(self) -> None:
        self.client = get_supabase_admin()
        self.table = "users"

    def create_anonymous_session(self, ip_address: str | None = None) -> dict:
        """创建匿名会话"""
        session_token = secrets.token_urlsafe(32)
        response = self.client.table(self.table).insert({
            "user_type": "ANONYMOUS",
            "is_anonymous": True,
            "session_token": session_token,
            "ip_address": ip_address,
            "search_limit": 5,
            "search_count": 0,
        }).execute()

        if not response.data:
            raise AppError(AppErrorCode.INTERNAL_ERROR, "Failed to create session")
        return response.data[0]

    def register(self, email: str, password: str, name: str | None = None) -> dict:
        """用户注册"""
        existing = (
            self.client.table(self.table)
            .select("id")
            .eq("email", email)
            .maybe_single()
            .execute()
        )
        if existing.data:
            raise AppError(AppErrorCode.DUPLICATE, "Email already registered")

        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        response = self.client.table(self.table).insert({
            "email": email,
            "password_hash": password_hash,
            "name": name,
            "user_type": "REGISTERED",
            "is_anonymous": False,
            "search_limit": 20,
            "search_count": 0,
        }).execute()

        if not response.data:
            raise AppError(AppErrorCode.INTERNAL_ERROR, "Failed to register")
        return response.data[0]

    def login(self, email: str, password: str) -> dict:
        """用户登录"""
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("email", email)
            .maybe_single()
            .execute()
        )
        user = response.data

        if not user or not user.get("password_hash"):
            raise AppError(AppErrorCode.UNAUTHORIZED, "Invalid credentials")

        if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            raise AppError(AppErrorCode.UNAUTHORIZED, "Invalid credentials")

        return user

    def update_password(self, user_id: str, old_password: str, new_password: str) -> None:
        """更新密码"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise AppError(AppErrorCode.NOT_FOUND, "User not found")

        if not user.get("password_hash"):
            raise AppError(AppErrorCode.FORBIDDEN, "Anonymous users cannot change password")

        if not bcrypt.checkpw(old_password.encode(), user["password_hash"].encode()):
            raise AppError(AppErrorCode.UNAUTHORIZED, "Invalid old password")

        new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        self.client.table(self.table).update({
            "password_hash": new_hash
        }).eq("id", user_id).execute()

    def get_user_by_id(self, user_id: str) -> dict | None:
        """根据 ID 获取用户"""
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("id", user_id)
            .maybe_single()
            .execute()
        )
        return response.data

    def get_user_by_session_token(self, session_token: str) -> dict | None:
        """根据 session token 获取用户"""
        response = (
            self.client.table(self.table)
            .select("*")
            .eq("session_token", session_token)
            .maybe_single()
            .execute()
        )
        return response.data

    def get_quota_status(self, user: dict) -> dict:
        """获取配额状态"""
        search_count = user.get("search_count", 0)
        search_limit = user.get("search_limit", 5)
        remaining = max(0, search_limit - search_count)
        return {
            "user_type": user.get("user_type"),
            "search_count": search_count,
            "search_limit": search_limit,
            "remaining": remaining,
            "quota_reset_at": user.get("quota_reset_at"),
        }

    def increment_search_count(self, user_id: str) -> None:
        """增加搜索计数"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise AppError(AppErrorCode.NOT_FOUND, "User not found")

        if user.get("search_count", 0) >= user.get("search_limit", 5):
            raise AppError(AppErrorCode.FORBIDDEN, "Search quota exceeded")

        self.client.table(self.table).update({
            "search_count": user.get("search_count", 0) + 1,
            "last_search_at": datetime.now(timezone.utc).isoformat(),
        }).eq("id", user_id).execute()

    @staticmethod
    def create_access_token(user_id: str, user_type: str) -> str:
        """创建访问 token"""
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
        payload = {
            "sub": user_id,
            "user_type": user_type,
            "type": "user",
            "exp": expire,
        }
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    @staticmethod
    def create_refresh_token(user_id: str) -> str:
        """创建刷新 token"""
        expire = datetime.now(timezone.utc) + timedelta(days=7)
        payload = {
            "sub": user_id,
            "type": "refresh",
            "exp": expire,
        }
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    @staticmethod
    def verify_token(token: str) -> dict:
        """验证 token"""
        try:
            payload = jwt.decode(
                token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AppError(AppErrorCode.UNAUTHORIZED, "Token expired")
        except jwt.InvalidTokenError:
            raise AppError(AppErrorCode.UNAUTHORIZED, "Invalid token")

    @staticmethod
    def verify_refresh_token(token: str) -> dict:
        """验证刷新 token"""
        payload = AuthService.verify_token(token)
        if payload.get("type") != "refresh":
            raise AppError(AppErrorCode.UNAUTHORIZED, "Invalid refresh token")
        return payload
