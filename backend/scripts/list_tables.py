"""
列出 Supabase 数据库中的所有表

使用方式：
    cd backend
    uv run python scripts/list_tables.py
"""
import asyncio
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from src.common.config import get_settings

settings = get_settings()


def clean_db_url(url: str) -> tuple[str, bool]:
    """移除 pgbouncer 参数并返回清理后的 URL 和是否使用 pgbouncer"""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    is_pgbouncer = "pgbouncer" in query_params
    query_params.pop("pgbouncer", None)
    new_query = urlencode(query_params, doseq=True)
    clean_url = urlunparse(parsed._replace(query=new_query))
    return clean_url, is_pgbouncer


async def list_tables():
    """列出所有表"""
    
    db_url = settings.supabase_db_url
    if not db_url:
        print("错误: SUPABASE_DB_URL 未配置")
        return
    
    # 清理 URL 并检查是否使用 pgbouncer
    db_url, is_pgbouncer = clean_db_url(db_url)
    
    # 转换为 asyncpg 格式
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")
    
    engine = create_async_engine(
        db_url,
        connect_args={
            "prepared_statement_cache_size": 0,
            "statement_cache_size": 0,
        } if is_pgbouncer else {},
    )
    
    async with engine.begin() as conn:
        # 获取所有表名
        result = await conn.execute(text("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename
        """))
        tables = [row[0] for row in result.fetchall()]
        
        if not tables:
            print("数据库中没有表")
        else:
            print(f"发现 {len(tables)} 个表:\n")
            for table in tables:
                print(f"  - {table}")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(list_tables())
