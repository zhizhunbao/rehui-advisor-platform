# 用户种子数据
import hashlib
from typing import Any, Dict, List


def hash_password(password: str) -> str:
    """哈希密码"""
    return hashlib.sha256(password.encode()).hexdigest()


ADMIN_USERS: List[Dict[str, Any]] = [
    {
        "username": "admin",
        "email": "admin@example.com",
        "name": "系统管理员",
        "role": "super_admin",
        "password_hash": hash_password("admin123"),
        "is_active": True,
    },
]

MEMBER_USERS: List[Dict[str, Any]] = [
    {
        "email": "demo@example.com",
        "name": "演示用户",
        "password_hash": hash_password("demo123"),
        "is_active": True,
    },
]
