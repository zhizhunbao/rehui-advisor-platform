"""管理员认证服务 - 使用 Document Store"""
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from src.common.document import DocumentStore
from src.common.errors import AppError, AppErrorCode
from src.common.config import get_settings

settings = get_settings()


DOC_TYPE = "admin_user"


class AdminAuthService:
    def __init__(self) -> None:
        self.store = DocumentStore()

    def login(self, username: str, password: str) -> dict:
        """管理员登录"""
        docs = self.store.find(DOC_TYPE, status="active")
        admin = None
        admin_doc = None
        
        for doc in docs:
            data = doc["data"]
            if data.get("username") == username or data.get("email") == username:
                admin = data
                admin_doc = doc
                break

        if not admin:
            raise AppError(AppErrorCode.UNAUTHORIZED, "Invalid credentials")

        if not admin.get("is_active"):
            raise AppError(AppErrorCode.FORBIDDEN, "Account is disabled")

        if not bcrypt.checkpw(password.encode(), admin["password_hash"].encode()):
            raise AppError(AppErrorCode.UNAUTHORIZED, "Invalid credentials")

        # 更新最后登录时间
        self.store.update(admin_doc["id"], data_updates={
            "last_login_at": datetime.now(timezone.utc).isoformat()
        })

        return self._to_response(admin_doc)

    def get_by_id(self, admin_id: str) -> dict | None:
        """根据 ID 获取管理员"""
        doc = self.store.get(admin_id)
        if not doc or doc["type"] != DOC_TYPE or doc["status"] == "deleted":
            return None
        return self._to_response(doc)

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
        docs = self.store.find(DOC_TYPE, status="active")
        for doc in docs:
            data = doc["data"]
            if data.get("username") == username or data.get("email") == email:
                raise AppError(AppErrorCode.DUPLICATE, "Username or email already exists")

        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        doc = self.store.create(DOC_TYPE, {
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "name": name,
            "role": role,
            "is_active": True,
            "last_login_at": None,
        })

        return self._to_response(doc)

    def update_password(
        self, admin_id: str, old_password: str, new_password: str
    ) -> None:
        """更新管理员密码"""
        doc = self.store.get(admin_id)
        if not doc or doc["type"] != DOC_TYPE or doc["status"] == "deleted":
            raise AppError(AppErrorCode.NOT_FOUND, "Admin not found")

        admin = doc["data"]
        if not bcrypt.checkpw(old_password.encode(), admin["password_hash"].encode()):
            raise AppError(AppErrorCode.UNAUTHORIZED, "Invalid old password")

        new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        self.store.update(admin_id, data_updates={"password_hash": new_hash})

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

    def _to_response(self, doc: dict) -> dict:
        """转换为响应格式（不包含密码）"""
        if not doc:
            return None
        data = doc["data"]
        return {
            "id": doc["id"],
            "username": data.get("username"),
            "email": data.get("email"),
            "name": data.get("name"),
            "role": data.get("role"),
            "is_active": data.get("is_active", True),
            "last_login_at": data.get("last_login_at"),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        }
