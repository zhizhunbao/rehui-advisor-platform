"""add github_links table

Revision ID: add_github_links_table
Revises: add_prompt_source_fields_001
Create Date: 2024-12-30
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = 'add_github_links_table'
down_revision = 'add_prompt_source_fields_001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'github_links',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('url', sa.String(500), nullable=False, unique=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('owner', sa.String(100), nullable=True),  # GitHub owner/org
        sa.Column('repo', sa.String(200), nullable=True),   # repo name
        sa.Column('path', sa.String(500), nullable=True),   # path within repo
        sa.Column('branch', sa.String(100), nullable=True, server_default='main'),
        
        # 分类和标签
        sa.Column('category', sa.String(50), nullable=True),  # skills, prompts, tools, docs, etc.
        sa.Column('subcategory', sa.String(50), nullable=True),
        sa.Column('tags', sa.ARRAY(sa.String), nullable=True),
        
        # 状态追踪
        sa.Column('status', sa.String(20), nullable=False, server_default='active'),  # active, archived, invalid, pending
        sa.Column('last_checked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_updated_at', sa.DateTime(timezone=True), nullable=True),  # GitHub repo last update
        sa.Column('check_error', sa.Text, nullable=True),
        
        # GitHub 元数据
        sa.Column('stars', sa.Integer, nullable=True),
        sa.Column('forks', sa.Integer, nullable=True),
        sa.Column('open_issues', sa.Integer, nullable=True),
        sa.Column('license', sa.String(50), nullable=True),
        sa.Column('language', sa.String(50), nullable=True),
        sa.Column('topics', sa.ARRAY(sa.String), nullable=True),
        
        # 内容分析
        sa.Column('has_skill_md', sa.Boolean, nullable=True),
        sa.Column('has_readme', sa.Boolean, nullable=True),
        sa.Column('file_count', sa.Integer, nullable=True),
        sa.Column('content_preview', sa.Text, nullable=True),  # 内容摘要
        
        # 评估
        sa.Column('quality_score', sa.Integer, nullable=True),  # 0-100
        sa.Column('is_featured', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('notes', sa.Text, nullable=True),  # 管理员备注
        
        # 关联
        sa.Column('synced_to', sa.String(50), nullable=True),  # skills, prompts, etc.
        sa.Column('synced_id', UUID(as_uuid=True), nullable=True),
        
        # 时间戳
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )
    
    # 索引
    op.create_index('ix_github_links_category', 'github_links', ['category'])
    op.create_index('ix_github_links_status', 'github_links', ['status'])
    op.create_index('ix_github_links_owner', 'github_links', ['owner'])
    op.create_index('ix_github_links_stars', 'github_links', ['stars'])


def downgrade() -> None:
    op.drop_table('github_links')
