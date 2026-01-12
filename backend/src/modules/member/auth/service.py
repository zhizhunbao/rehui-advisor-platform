"""用户认证服务 - 使用 Document Store"""
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from src.common.config import get_settings

settings = get_settings()


DOC_TYPE = "member_user"


class AuthService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def create_anonymous_session(self, ip_address: str | None = None) -> dict:
        """创建匿名会话"""
        session_token = secrets.token_urlsafe(32)
        doc = self.store.create(DOC_TYPE, {
            "user_type": "ANONYMOUS",
            "is_anonymous": True,
            "session_token": session_token,
            "ip_address": ip_address,
            "search_limit": 5,
            "search_count": 0,
        })
        return self._to_response(doc)

    def register(self, email: str, password: str, name: str | None = None) -> dict:
        """用户注册"""
        existing = self._find_by_email(email)
        if existing:
            raise AppError(AppErrorCode.DUPLICATE, "Email already registered")

        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        doc = self.store.create(DOC_TYPE, {
            "email": email,
            "password_hash": password_hash,
            "name": name,
            "user_type": "REGISTERED",
            "is_anonymous": False,
            "search_limit": 20,
            "search_count": 0,
        })
        return self._to_response(doc)

    def login(self, email: str, password: str) -> dict:
        """用户登录"""
        doc = self._find_by_email(email)
        if not doc:
            raise AppError(AppErrorCode.UNAUTHORIZED, "Invalid credentials")

        user = doc["data"]
        if not user.get("password_hash"):
            raise AppError(AppErrorCode.UNAUTHORIZED, "Invalid credentials")

        if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            raise AppError(AppErrorCode.UNAUTHORIZED, "Invalid credentials")

        return self._to_response(doc)

    def update_password(self, user_id: str, old_password: str, new_password: str) -> None:
        """更新密码"""
        doc = self.store.get(user_id)
        if not doc or doc["type"] != DOC_TYPE or doc["status"] == "deleted":
            raise AppError(AppErrorCode.NOT_FOUND, "User not found")

        user = doc["data"]
        if not user.get("password_hash"):
            raise AppError(AppErrorCode.FORBIDDEN, "Anonymous users cannot change password")

        if not bcrypt.checkpw(old_password.encode(), user["password_hash"].encode()):
            raise AppError(AppErrorCode.UNAUTHORIZED, "Invalid old password")

        new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        self.store.update(user_id, data_updates={"password_hash": new_hash})

    def get_user_by_id(self, user_id: str) -> dict | None:
        """根据 ID 获取用户"""
        doc = self.store.get(user_id)
        if not doc or doc["type"] != DOC_TYPE or doc["status"] == "deleted":
            return None
        return self._to_response(doc)

    def get_user_by_session_token(self, session_token: str) -> dict | None:
        """根据 session token 获取用户"""
        docs = self.store.find(DOC_TYPE, status="active")
        for doc in docs:
            if doc["data"].get("session_token") == session_token:
                return self._to_response(doc)
        return None

    def _find_by_email(self, email: str) -> dict | None:
        """根据邮箱查找用户文档"""
        docs = self.store.find(DOC_TYPE, status="active")
        for doc in docs:
            if doc["data"].get("email") == email:
                return doc
        return None

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
        doc = self.store.get(user_id)
        if not doc or doc["type"] != DOC_TYPE or doc["status"] == "deleted":
            raise AppError(AppErrorCode.NOT_FOUND, "User not found")

        user = doc["data"]
        if user.get("search_count", 0) >= user.get("search_limit", 5):
            raise AppError(AppErrorCode.FORBIDDEN, "Search quota exceeded")

        self.store.update(user_id, data_updates={
            "search_count": user.get("search_count", 0) + 1,
            "last_search_at": datetime.now(timezone.utc).isoformat(),
        })

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

    def _to_response(self, doc: dict) -> dict:
        """转换为响应格式（不包含密码）"""
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "email": data.get("email"),
            "name": data.get("name"),
            "user_type": data.get("user_type"),
            "is_anonymous": data.get("is_anonymous"),
            "session_token": data.get("session_token"),
            "ip_address": data.get("ip_address"),
            "search_limit": data.get("search_limit"),
            "search_count": data.get("search_count"),
            "last_search_at": data.get("last_search_at"),
            "quota_reset_at": data.get("quota_reset_at"),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        }
