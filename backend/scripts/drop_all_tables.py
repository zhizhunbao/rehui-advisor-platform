"""Drop all tables in the database."""
import asyncio
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from src.common.config import get_settings


def clean_db_url(url: str) -> tuple[str, bool]:
    """移除 pgbouncer 参数并返回清理后的 URL 和是否使用 pgbouncer"""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    is_pgbouncer = "pgbouncer" in query_params
    query_params.pop("pgbouncer", None)
    new_query = urlencode(query_params, doseq=True)
    clean_url = urlunparse(parsed._replace(query=new_query))
    return clean_url, is_pgbouncer


async def drop_all():
    settings = get_settings()
    db_url = settings.supabase_db_url
    if not db_url:
        print("错误: SUPABASE_DB_URL 未配置")
        return
    
    db_url, is_pgbouncer = clean_db_url(db_url)
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")
    
    engine = create_async_engine(
        db_url,
        connect_args={
            "prepared_statement_cache_size": 0,
            "statement_cache_size": 0,
        } if is_pgbouncer else {},
    )
    
    async with engine.begin() as conn:
        # Drop and recreate public schema
        await conn.execute(text("DROP SCHEMA public CASCADE"))
        await conn.execute(text("CREATE SCHEMA public"))
        await conn.execute(text("GRANT ALL ON SCHEMA public TO postgres"))
        await conn.execute(text("GRANT ALL ON SCHEMA public TO public"))
        print("All tables dropped!")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(drop_all())
