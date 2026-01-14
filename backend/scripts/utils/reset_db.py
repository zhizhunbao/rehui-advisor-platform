# 数据库管理脚本 - 重置数据库
import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from scripts.base import ScriptBase, ScriptResult


class ResetDbScript(ScriptBase):
    """重置数据库"""

    NAME = "重置数据库"
    DESCRIPTION = "删除所有表并重置数据库（仅用于开发环境）"

    def run(self) -> ScriptResult:
        """执行重置"""
        return asyncio.run(self._reset())

    async def _reset(self) -> ScriptResult:
        """异步执行重置"""
        settings = self.get_settings()
        db_url = settings.supabase_db_url

        if not db_url:
            self.error("SUPABASE_DB_URL 未配置")
            return ScriptResult(success=False, message="DB URL not configured")

        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

        engine = create_async_engine(
            db_url,
            echo=False,
            connect_args={
                "prepared_statement_cache_size": 0,
                "statement_cache_size": 0,
            } if "pgbouncer=true" in db_url else {},
        )

        try:
            async with engine.begin() as conn:
                result = await conn.execute(text("""
                    SELECT tablename FROM pg_tables 
                    WHERE schemaname = 'public'
                """))
                tables = [row[0] for row in result.fetchall()]

                if not tables:
                    self.info("数据库中没有表")
                    return ScriptResult(success=True, message="No tables to delete")

                self.info(f"发现 {len(tables)} 个表")

                confirm = input("\n确认删除所有表？(yes/no): ")
                if confirm.lower() != "yes":
                    self.warning("已取消")
                    return ScriptResult(success=False, message="Cancelled")

                for table in tables:
                    self.info(f"删除表: {table}")
                    await conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))

                self.success(f"已删除 {len(tables)} 个表")
                return ScriptResult(success=True, message="Reset complete", deleted=len(tables))

        finally:
            await engine.dispose()


if __name__ == "__main__":
    script = ResetDbScript()
    result = script.run()
    exit(0 if result.success else 1)
