"""rename github_links to data_sources

Revision ID: rename_to_data_sources
Revises: drop_llm_region
Create Date: 2025-01-01

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'rename_to_data_sources'
down_revision: Union[str, None] = 'drop_llm_region'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 重命名表
    op.execute("ALTER TABLE github_links RENAME TO data_sources")
    
    # 添加 type 字段
    op.execute("""
        ALTER TABLE data_sources 
        ADD COLUMN IF NOT EXISTS type VARCHAR(20) DEFAULT 'github'
    """)
    
    # 添加 config 字段（用于存储 API key 等配置）
    op.execute("""
        ALTER TABLE data_sources 
        ADD COLUMN IF NOT EXISTS config JSONB DEFAULT '{}'
    """)
    
    # 添加注释
    op.execute("COMMENT ON TABLE data_sources IS '数据源管理表，支持多种来源类型'")
    op.execute("COMMENT ON COLUMN data_sources.type IS '来源类型: github, api, website, rss'")
    op.execute("COMMENT ON COLUMN data_sources.category IS '业务领域: llm-models, flight, hotel, job'")
    op.execute("COMMENT ON COLUMN data_sources.config IS '配置信息，如 API 认证等'")


def downgrade() -> None:
    op.execute("ALTER TABLE data_sources DROP COLUMN IF EXISTS config")
    op.execute("ALTER TABLE data_sources DROP COLUMN IF EXISTS type")
    op.execute("ALTER TABLE data_sources RENAME TO github_links")
