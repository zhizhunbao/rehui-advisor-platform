"""add retrieval engines tables

Revision ID: add_retrieval_engines
Revises: rename_to_data_sources
Create Date: 2024-12-31

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = 'add_retrieval_engines'
down_revision: Union[str, None] = 'rename_to_data_sources'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 检索引擎表
    op.create_table(
        'retrieval_engines',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False, unique=True, comment='引擎标识'),
        sa.Column('display_name', sa.String(200), nullable=False, comment='显示名称'),
        sa.Column('type', sa.String(50), nullable=False, comment='引擎类型: keyword_match, structured_query, rag_vector, page_index, agent_tools, realtime_search, hybrid'),
        sa.Column('description', sa.Text(), comment='描述'),
        sa.Column('config', postgresql.JSONB(), server_default='{}', comment='引擎配置'),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('is_default', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('idx_retrieval_engines_type', 'retrieval_engines', ['type'])
    op.create_index('idx_retrieval_engines_active', 'retrieval_engines', ['is_active'])

    # 领域配置表
    op.create_table(
        'retrieval_domain_configs',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('domain', sa.String(50), nullable=False, unique=True, comment='领域: job, education, investment, insurance, house, car, hotel, flight'),
        sa.Column('engine_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('retrieval_engines.id', ondelete='CASCADE'), nullable=False),
        sa.Column('config', postgresql.JSONB(), server_default='{}', comment='领域特定配置覆盖'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('idx_retrieval_domain_configs_domain', 'retrieval_domain_configs', ['domain'])

    # 更新时间触发器
    op.execute("""
        CREATE OR REPLACE FUNCTION update_retrieval_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER trigger_retrieval_engines_updated_at
            BEFORE UPDATE ON retrieval_engines
            FOR EACH ROW EXECUTE FUNCTION update_retrieval_updated_at();
    """)

    op.execute("""
        CREATE TRIGGER trigger_retrieval_domain_configs_updated_at
            BEFORE UPDATE ON retrieval_domain_configs
            FOR EACH ROW EXECUTE FUNCTION update_retrieval_updated_at();
    """)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trigger_retrieval_domain_configs_updated_at ON retrieval_domain_configs")
    op.execute("DROP TRIGGER IF EXISTS trigger_retrieval_engines_updated_at ON retrieval_engines")
    op.execute("DROP FUNCTION IF EXISTS update_retrieval_updated_at()")
    op.drop_table('retrieval_domain_configs')
    op.drop_table('retrieval_engines')
