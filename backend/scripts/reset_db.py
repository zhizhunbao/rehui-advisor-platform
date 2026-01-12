"""
重置 Supabase 数据库

警告：此脚本会删除所有表和数据！仅用于开发环境。

使用方式：
    cd backend
    uv run python scripts/reset_db.py
"""
import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from src.common.config import get_settings

settings = get_settings()


async def reset_database():
    """删除所有表并重置 alembic 版本"""
    
    db_url = settings.supabase_db_url
    if not db_url:
        print("错误: SUPABASE_DB_URL 未配置")
        return
    
    # 转换为 asyncpg 格式
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")
    
    engine = create_async_engine(
        db_url,
        echo=True,
        connect_args={
            "prepared_statement_cache_size": 0,
            "statement_cache_size": 0,
        } if "pgbouncer=true" in db_url else {},
    )
    
    async with engine.begin() as conn:
        # 获取所有表名（排除系统表）
        result = await conn.execute(text("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public'
        """))
        tables = [row[0] for row in result.fetchall()]
        
        if not tables:
            print("数据库中没有表")
            return
        
        print(f"发现 {len(tables)} 个表: {tables}")
        
        # 确认删除
        confirm = input("\n确认删除所有表？(yes/no): ")
        if confirm.lower() != "yes":
            print("已取消")
            return
        
        # 删除所有表（级联删除）
        for table in tables:
            print(f"删除表: {table}")
            await conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
        
        print("\n所有表已删除")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(reset_database())
