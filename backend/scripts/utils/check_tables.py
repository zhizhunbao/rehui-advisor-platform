# 检查脚本 - 检查数据库表
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from sqlalchemy import create_engine, text

from scripts.base import CheckScript


def clean_db_url(url: str) -> str:
    """移除 pgbouncer 参数"""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    query_params.pop("pgbouncer", None)
    new_query = urlencode(query_params, doseq=True)
    return urlunparse(parsed._replace(query=new_query))


class CheckTablesScript(CheckScript):
    """检查数据库表"""

    NAME = "数据库表检查"
    DESCRIPTION = "列出数据库中的所有表"

    def check(self) -> bool:
        """执行检查"""
        settings = self.get_settings()
        db_url = settings.supabase_db_url or settings.database_url

        if not db_url:
            self.error("数据库 URL 未配置")
            return False

        db_url = clean_db_url(db_url)
        db_url = db_url.replace("postgresql://", "postgresql+psycopg://")

        engine = create_engine(db_url)

        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """))

            tables = [row[0] for row in result]

            self.info(f"数据库中共有 {len(tables)} 个表:")
            for table in tables:
                self.info(f"  - {table}")

        return len(tables) > 0


if __name__ == "__main__":
    script = CheckTablesScript()
    result = script.run()
    exit(0 if result.success else 1)
