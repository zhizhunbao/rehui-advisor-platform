# 检查数据库连接和表结构
import asyncio
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from scripts.base import CheckScript


class CheckDbScript(CheckScript):
    """检查数据库连接和表结构"""

    NAME = "数据库检查"
    DESCRIPTION = "验证数据库连接和核心表是否存在"

    def check(self) -> bool:
        """执行检查"""
        return asyncio.run(self._async_check())

    async def _async_check(self) -> bool:
        """异步检查数据库"""
        settings = self.get_settings()
        db_url = settings.supabase_db_url

        if not db_url:
            self.error("SUPABASE_DB_URL 未配置")
            return False

        db_url = self._clean_db_url(db_url)
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

        engine = create_async_engine(db_url)

        try:
            async with engine.connect() as conn:
                result = await conn.execute(text("""
                    SELECT table_schema, table_name 
                    FROM information_schema.tables 
                    WHERE table_name IN ('admin_users', 'subscription_plans', 'system_configs', 'users', 'documents')
                """))
                rows = result.fetchall()

                self.info("找到的表:")
                for row in rows:
                    self.info(f"  - {row[0]}.{row[1]}")

                if not rows:
                    self.warning("没有找到任何表!")
                    return False

                return True
        finally:
            await engine.dispose()

    def _clean_db_url(self, url: str) -> str:
        """移除 pgbouncer 参数"""
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        query_params.pop("pgbouncer", None)
        new_query = urlencode(query_params, doseq=True)
        return urlunparse(parsed._replace(query=new_query))


if __name__ == "__main__":
    script = CheckDbScript()
    result = script.run()
    exit(0 if result.success else 1)
