"""检查数据库中的表"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
from sqlalchemy import create_engine, text
from src.common.config import get_settings

def clean_db_url(url: str) -> str:
    """移除 pgbouncer 参数"""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    query_params.pop("pgbouncer", None)
    new_query = urlencode(query_params, doseq=True)
    return urlunparse(parsed._replace(query=new_query))

settings = get_settings()
DATABASE_URL = settings.supabase_db_url or settings.database_url
DATABASE_URL = clean_db_url(DATABASE_URL)
DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """))
    
    tables = [row[0] for row in result]
    
    print(f"数据库中共有 {len(tables)} 个表:")
    for table in tables:
        print(f"  - {table}")
