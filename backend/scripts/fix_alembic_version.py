"""修复 alembic_version 表"""
import sys
sys.path.insert(0, ".")

from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
from sqlalchemy import create_engine, text
from src.common.config import get_settings

def clean_db_url(url):
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    query_params.pop('pgbouncer', None)
    return urlunparse(parsed._replace(query=urlencode(query_params, doseq=True)))

settings = get_settings()
db_url = clean_db_url(settings.supabase_db_url or settings.database_url)
db_url = db_url.replace('postgresql://', 'postgresql+psycopg://')
engine = create_engine(db_url)

with engine.connect() as conn:
    conn.execute(text("DELETE FROM alembic_version"))
    conn.execute(text("INSERT INTO alembic_version (version_num) VALUES ('add_documents_table_001')"))
    conn.commit()
    print('alembic_version 已更新为 add_documents_table_001')
