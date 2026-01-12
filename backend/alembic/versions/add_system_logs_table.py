"""add system logs table

Revision ID: add_system_logs_table
Revises: add_scheduler_tables
Create Date: 2024-12-31

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = 'add_system_logs_table'
down_revision: Union[str, None] = 'add_scheduler_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 系统日志表
    op.create_table(
        'system_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('level', sa.String(20), nullable=False, comment='日志级别: debug, info, warn, error'),
        sa.Column('module', sa.String(100), comment='模块名称'),
        sa.Column('message', sa.Text(), nullable=False, comment='日志消息'),
        sa.Column('extra', postgresql.JSONB(), server_default='{}', comment='额外数据'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('idx_system_logs_level', 'system_logs', ['level'])
    op.create_index('idx_system_logs_module', 'system_logs', ['module'])
    op.create_index('idx_system_logs_created_at', 'system_logs', ['created_at'])

    # 禁用 RLS
    op.execute("ALTER TABLE system_logs DISABLE ROW LEVEL SECURITY")

    # 授予权限
    op.execute("GRANT ALL ON system_logs TO postgres, service_role")


def downgrade() -> None:
    op.drop_table('system_logs')
