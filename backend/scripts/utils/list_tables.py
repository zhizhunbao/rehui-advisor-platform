# 数据库管理脚本 - 列出所有表
import asyncio
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from scripts.base import ScriptBase, ScriptResult


def clean_db_url(url: str) -> tuple[str, bool]:
    """移除 pgbouncer 参数并返回清理后的 URL 和是否使用 pgbouncer"""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    is_pgbouncer = "pgbouncer" in query_params
    query_params.pop("pgbouncer", None)
    new_query = urlencode(query_params, doseq=True)
    clean_url = urlunparse(parsed._replace(query=new_query))
    return clean_url, is_pgbouncer


class ListTablesScript(ScriptBase):
    """列出数据库表"""

    NAME = "列出数据库表"
    DESCRIPTION = "列出 Supabase 数据库中的所有表"

    def run(self) -> ScriptResult:
        """执行列表"""
        return asyncio.run(self._list())

    async def _list(self) -> ScriptResult:
        """异步执行列表"""
        settings = self.get_settings()
        db_url = settings.supabase_db_url

        if not db_url:
            self.error("SUPABASE_DB_URL 未配置")
            return ScriptResult(success=False, message="DB URL not configured")

        db_url, is_pgbouncer = clean_db_url(db_url)
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

        engine = create_async_engine(
            db_url,
            connect_args={
                "prepared_statement_cache_size": 0,
                "statement_cache_size": 0,
            } if is_pgbouncer else {},
        )

        try:
            async with engine.begin() as conn:
                result = await conn.execute(text("""
                    SELECT tablename FROM pg_tables 
                    WHERE schemaname = 'public'
                    ORDER BY tablename
                """))
                tables = [row[0] for row in result.fetchall()]

                if not tables:
                    self.info("数据库中没有表")
                else:
                    self.info(f"发现 {len(tables)} 个表:\n")
                    for table in tables:
                        print(f"  - {table}")

                return ScriptResult(success=True, message=f"Found {len(tables)} tables")

        finally:
            await engine.dispose()


if __name__ == "__main__":
    script = ListTablesScript()
    result = script.run()
    exit(0 if result.success else 1)
