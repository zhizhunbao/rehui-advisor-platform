"""add discovery_keywords to domains

Revision ID: add_discovery_keywords
Revises: add_scheduler_tables
Create Date: 2024-12-31

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = 'add_discovery_keywords'
down_revision: Union[str, None] = 'add_scheduler_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 给 domains 表添加 discovery_keywords 字段
    op.add_column(
        'domains',
        sa.Column(
            'discovery_keywords',
            postgresql.ARRAY(sa.Text()),
            server_default='{}',
            nullable=True,
            comment='领域探索关键词列表，用于 GitHub 自动发现'
        )
    )


def downgrade() -> None:
    op.drop_column('domains', 'discovery_keywords')
