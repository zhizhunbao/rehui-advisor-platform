"""检查数据库表"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from src.common.config import get_settings

settings = get_settings()


async def main():
    db_url = settings.supabase_db_url
    if not db_url:
        print("错误: SUPABASE_DB_URL 未配置")
        return

    # 移除 pgbouncer 参数
    if "pgbouncer" in db_url:
        db_url = db_url.replace("?pgbouncer=true", "").replace("&pgbouncer=true", "")
    
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")
    
    engine = create_async_engine(db_url)
    
    async with engine.connect() as conn:
        # 检查表是否存在
        result = await conn.execute(text("""
            SELECT table_schema, table_name 
            FROM information_schema.tables 
            WHERE table_name IN ('admin_users', 'subscription_plans', 'system_configs', 'users')
        """))
        rows = result.fetchall()
        
        print("找到的表:")
        for row in rows:
            print(f"  - {row[0]}.{row[1]}")
        
        if not rows:
            print("  没有找到任何表!")
        
        # 检查表权限
        result = await conn.execute(text("""
            SELECT grantee, table_name, privilege_type
            FROM information_schema.table_privileges
            WHERE table_name IN ('admin_users', 'subscription_plans', 'system_configs', 'users')
            AND grantee IN ('anon', 'authenticated', 'service_role')
        """))
        rows = result.fetchall()
        
        print("\n表权限:")
        for row in rows:
            print(f"  - {row[0]} -> {row[1]}: {row[2]}")
        
        if not rows:
            print("  没有找到任何权限配置!")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
