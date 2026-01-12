from logging.config import fileConfig
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from alembic import context
from sqlalchemy import pool, create_engine, MetaData
from sqlalchemy.engine import Connection

from src.common.config import get_settings

config = context.config
settings = get_settings()

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 使用空的 metadata，因为我们使用 Document Store 模式
target_metadata = MetaData()


def clean_db_url(url: str) -> str:
    """移除 pgbouncer 参数并返回清理后的 URL"""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    query_params.pop("pgbouncer", None)
    new_query = urlencode(query_params, doseq=True)
    clean_url = urlunparse(parsed._replace(query=new_query))
    return clean_url


def get_url() -> str:
    """获取数据库 URL，使用同步驱动 psycopg"""
    db_url = settings.supabase_db_url or settings.database_url
    if not db_url:
        raise ValueError("No database URL configured")
    db_url = clean_db_url(db_url)
    # 使用同步驱动 psycopg (psycopg3)
    return db_url.replace("postgresql://", "postgresql+psycopg://")


def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    url = get_url()
    connectable = create_engine(
        url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        do_run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
