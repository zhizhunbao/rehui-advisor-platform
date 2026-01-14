# 数据库管理脚本 - 授予权限
import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from scripts.base import ScriptBase, ScriptResult


class GrantPermissionsScript(ScriptBase):
    """授予数据库权限"""

    NAME = "授予权限"
    DESCRIPTION = "授予 Supabase 角色权限"

    def run(self) -> ScriptResult:
        """执行授权"""
        return asyncio.run(self._grant())

    async def _grant(self) -> ScriptResult:
        """异步执行授权"""
        settings = self.get_settings()
        db_url = settings.supabase_db_url

        if not db_url:
            self.error("SUPABASE_DB_URL 未配置")
            return ScriptResult(success=False, message="DB URL not configured")

        if "pgbouncer" in db_url:
            db_url = db_url.replace("?pgbouncer=true", "").replace("&pgbouncer=true", "")

        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

        engine = create_async_engine(db_url)
        granted = 0
        errors = []

        try:
            async with engine.begin() as conn:
                self.info("授予 service_role 完全权限...")
                try:
                    await conn.execute(text("GRANT ALL ON documents TO service_role"))
                    self.info("  ✓ documents")
                    granted += 1
                except Exception as e:
                    errors.append(f"documents: {e}")

                self.info("\n授予 authenticated 读取权限...")
                try:
                    await conn.execute(text("GRANT SELECT ON documents TO authenticated"))
                    self.info("  ✓ documents")
                except Exception as e:
                    errors.append(f"documents: {e}")

            self.success(f"权限授予完成，成功 {granted} 个表")
            return ScriptResult(success=True, message="Permissions granted", updated=granted, errors=errors if errors else None)

        finally:
            await engine.dispose()


if __name__ == "__main__":
    script = GrantPermissionsScript()
    result = script.run()
    exit(0 if result.success else 1)
