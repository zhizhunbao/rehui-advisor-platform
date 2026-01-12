"""
Supabase 客户端模块

提供两种客户端：
- 普通客户端（anon key）：用于前端可访问的操作
- 管理员客户端（service_role_key）：用于绑过 RLS 的后端操作

使用方式参考：supabase_guidelines.md
API 参考：SUPABASE_PYTHON_API.md
"""
from typing import Any

from src.common.config import get_settings

settings = get_settings()

# 客户端单例
_supabase_client: Any = None
_supabase_admin_client: Any = None


def get_supabase() -> Any:
    """
    获取 Supabase 客户端（使用 anon key）
    
    用途：
    - 受 RLS 保护的数据库操作
    - Supabase Auth
    - Supabase Storage（公开访问）
    - Supabase Realtime
    
    示例：
        client = get_supabase()
        response = client.table("users").select("*").execute()
    """
    global _supabase_client
    if _supabase_client is None:
        if not settings.supabase_url or not settings.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY are required")
        from supabase import create_client
        _supabase_client = create_client(settings.supabase_url, settings.supabase_key)
    return _supabase_client


def get_supabase_admin() -> Any:
    """
    获取 Supabase 管理员客户端（使用 service_role_key）
    
    用途：
    - 绑过 RLS 的数据库操作
    - Auth Admin API（创建/删除用户等）
    - Storage 管理操作
    
    注意：此客户端拥有完全权限，仅在后端使用
    
    示例：
        admin = get_supabase_admin()
        response = admin.auth.admin.list_users()
    """
    global _supabase_admin_client
    if _supabase_admin_client is None:
        if not settings.supabase_url or not settings.supabase_service_key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY are required")
        from supabase import create_client
        _supabase_admin_client = create_client(
            settings.supabase_url,
            settings.supabase_service_key,
        )
    return _supabase_admin_client
