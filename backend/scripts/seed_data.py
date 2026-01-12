"""
种子数据脚本 - 创建初始数据

使用方式：
    cd backend
    uv run python scripts/seed_data.py
"""
import sys
import os

# 添加 backend 目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bcrypt
from supabase import create_client

from src.common.config import get_settings

settings = get_settings()


def hash_password(password: str) -> str:
    """使用 bcrypt 哈希密码"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def get_client():
    """获取 Supabase 客户端"""
    if not settings.supabase_url or not settings.supabase_service_key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY are required")
    return create_client(settings.supabase_url, settings.supabase_service_key)


def seed_admin_users(client) -> None:
    """创建初始超级管理员账户"""
    from postgrest.exceptions import APIError
    
    try:
        # 检查是否已存在
        response = (
            client.table("admin_users")
            .select("id")
            .eq("username", "admin")
            .execute()
        )
        
        if response.data and len(response.data) > 0:
            print("  - 超级管理员已存在，跳过")
            return

        # 创建管理员
        response = client.table("admin_users").insert({
            "username": "admin",
            "email": "admin@rehui.com",
            "password_hash": hash_password("admin123"),
            "name": "超级管理员",
            "role": "super_admin",
            "is_active": True,
        }).execute()

        if response.data:
            print("  - 创建超级管理员: admin / admin123")
        else:
            print("  - 创建超级管理员失败")
    except APIError as e:
        print(f"  - 创建超级管理员失败: {e}")
        print("    请确保 admin_users 表已创建，并且 RLS 策略允许 service_role 访问")


def seed_subscription_plans(client) -> None:
    """创建默认订阅方案"""
    from postgrest.exceptions import APIError
    
    try:
        # 检查是否已存在
        response = client.table("subscription_plans").select("id").limit(1).execute()
        
        if response.data and len(response.data) > 0:
            print("  - 订阅方案已存在，跳过")
            return

        plans = [
            {
                "name": "免费版",
                "name_en": "Free",
                "description": "基础功能，每日5次查询",
                "description_en": "Basic features, 5 queries per day",
                "price": 0.0,
                "currency": "USD",
                "billing_period": "monthly",
                "daily_quota": 5,
                "features": ["基础推荐", "历史记录"],
                "is_active": True,
                "sort_order": 0,
            },
            {
                "name": "专业版",
                "name_en": "Pro",
                "description": "高级功能，每日50次查询",
                "description_en": "Advanced features, 50 queries per day",
                "price": 9.99,
                "currency": "USD",
                "billing_period": "monthly",
                "daily_quota": 50,
                "features": ["基础推荐", "历史记录", "高级分析", "优先支持"],
                "is_active": True,
                "sort_order": 1,
            },
            {
                "name": "企业版",
                "name_en": "Enterprise",
                "description": "无限查询，专属支持",
                "description_en": "Unlimited queries, dedicated support",
                "price": 49.99,
                "currency": "USD",
                "billing_period": "monthly",
                "daily_quota": 9999,
                "features": ["基础推荐", "历史记录", "高级分析", "优先支持", "API访问", "专属客服"],
                "is_active": True,
                "sort_order": 2,
            },
        ]

        response = client.table("subscription_plans").insert(plans).execute()
        
        if response.data:
            print(f"  - 创建 {len(plans)} 个订阅方案")
        else:
            print("  - 创建订阅方案失败")
    except APIError as e:
        print(f"  - 创建订阅方案失败: {e}")


def seed_system_configs(client) -> None:
    """创建默认系统配置"""
    from postgrest.exceptions import APIError
    import json
    
    try:
        # 检查是否已存在
        response = client.table("system_configs").select("id").limit(1).execute()
        
        if response.data and len(response.data) > 0:
            print("  - 系统配置已存在，跳过")
            return

        configs = [
            {
                "key": "ai_model",
                "value": json.dumps("gemini-1.5-flash"),
                "description": "默认AI模型",
                "category": "ai",
                "is_sensitive": False,
            },
            {
                "key": "ai_temperature",
                "value": json.dumps(0.7),
                "description": "AI温度参数",
                "category": "ai",
                "is_sensitive": False,
            },
            {
                "key": "free_daily_quota",
                "value": json.dumps(5),
                "description": "免费用户每日查询次数",
                "category": "quota",
                "is_sensitive": False,
            },
            {
                "key": "maintenance_mode",
                "value": json.dumps(False),
                "description": "维护模式开关",
                "category": "feature",
                "is_sensitive": False,
            },
            {
                "key": "site_name",
                "value": json.dumps("Rehui Advisor"),
                "description": "网站名称",
                "category": "general",
                "is_sensitive": False,
            },
        ]

        response = client.table("system_configs").insert(configs).execute()
        
        if response.data:
            print(f"  - 创建 {len(configs)} 个系统配置")
        else:
            print("  - 创建系统配置失败")
    except APIError as e:
        print(f"  - 创建系统配置失败: {e}")


def check_tables(client) -> None:
    """检查表是否存在"""
    from postgrest.exceptions import APIError
    
    tables = ["admin_users", "subscription_plans", "system_configs", "users"]
    for table in tables:
        try:
            response = client.table(table).select("id").limit(1).execute()
            print(f"  ✓ 表 {table} 存在")
        except APIError as e:
            print(f"  ✗ 表 {table} 错误: {e.message}")


def main():
    """主函数"""
    print("开始创建种子数据...")
    
    try:
        client = get_client()
    except ValueError as e:
        print(f"错误: {e}")
        return

    print("\n检查表状态:")
    check_tables(client)
    
    print("\n创建数据:")
    seed_admin_users(client)
    seed_subscription_plans(client)
    seed_system_configs(client)

    print("\n种子数据创建完成!")


if __name__ == "__main__":
    main()
