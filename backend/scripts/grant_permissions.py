"""授予 Supabase 角色权限"""
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
    
    async with engine.begin() as conn:
        # 所有表
        all_tables = [
            'analysis_results', 'cars', 'cleaned_data', 'education', 'flights',
            'hotels', 'houses', 'insurance_claims', 'insurance_products',
            'insurance_providers', 'insurance_quotes', 'investments', 'jobs',
            'price_history', 'raw_data', 'recommendations', 'search_history', 'users',
            'admin_users', 'subscription_plans', 'system_configs',
            'refresh_tokens', 'password_reset_tokens', 'login_attempts'
        ]
        
        print("授予 service_role 完全权限...")
        for table in all_tables:
            try:
                await conn.execute(text(f"GRANT ALL ON {table} TO service_role"))
                print(f"  ✓ {table}")
            except Exception as e:
                print(f"  ✗ {table}: {e}")
        
        # 公开表授予 authenticated 和 anon 读取权限
        public_tables = ['flights', 'hotels', 'houses', 'cars', 'jobs', 'education', 'investments', 'subscription_plans']
        print("\n授予 authenticated/anon 读取权限...")
        for table in public_tables:
            try:
                await conn.execute(text(f"GRANT SELECT ON {table} TO authenticated"))
                await conn.execute(text(f"GRANT SELECT ON {table} TO anon"))
                print(f"  ✓ {table}")
            except Exception as e:
                print(f"  ✗ {table}: {e}")
    
    await engine.dispose()
    print("\n权限授予完成!")


if __name__ == "__main__":
    asyncio.run(main())
