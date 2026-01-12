"""add_skill_categories_table

Revision ID: add_skill_categories_001
Revises: add_skills_table_001
Create Date: 2025-12-30

Create skill_categories table for managing skill category/source labels.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "add_skill_categories_001"
down_revision: Union[str, None] = "add_skills_table_001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create skill_categories table
    op.create_table(
        "skill_categories",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("type", sa.String(20), nullable=False),  # category, source
        sa.Column("code", sa.String(50), nullable=False),
        sa.Column("label_zh", sa.String(100), nullable=False),
        sa.Column("label_en", sa.String(100), nullable=True),
        sa.Column("color", sa.String(50), nullable=True),
        sa.Column("icon", sa.String(50), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("type", "code", name="uq_skill_categories_type_code"),
    )
    op.create_index("ix_skill_categories_type", "skill_categories", ["type"], unique=False)

    # Grant permissions
    op.execute("GRANT ALL ON skill_categories TO service_role")
    op.execute("GRANT SELECT ON skill_categories TO authenticated")
    op.execute("GRANT SELECT ON skill_categories TO anon")

    # Insert initial category data
    op.execute("""
        INSERT INTO skill_categories (type, code, label_zh, label_en, sort_order) VALUES
        ('category', 'development', '开发工具', 'Development', 1),
        ('category', 'collaboration', '协作管理', 'Collaboration', 2),
        ('category', 'learning', '学习知识', 'Learning', 3),
        ('category', 'security', '安全测试', 'Security', 4),
        ('category', 'design', '设计创意', 'Design', 5),
        ('category', 'document', '文档处理', 'Document', 6),
        ('category', 'writing', '写作研究', 'Writing', 7),
        ('category', 'automation', '自动化', 'Automation', 8),
        ('category', 'media', '媒体内容', 'Media', 9),
        ('category', 'data', '数据分析', 'Data', 10),
        ('category', 'communication', '沟通协作', 'Communication', 11),
        ('category', 'science', '科学计算', 'Science', 12),
        ('category', 'tool', '实用工具', 'Tool', 13),
        ('category', 'visualization', '数据可视化', 'Visualization', 14)
    """)

    # Insert initial source data
    op.execute("""
        INSERT INTO skill_categories (type, code, label_zh, label_en, color, sort_order) VALUES
        ('source', 'official', '官方', 'Official', 'amber', 1),
        ('source', 'community', '社区', 'Community', 'green', 2),
        ('source', 'claude-code', 'Claude Code', 'Claude Code', 'blue', 3)
    """)


def downgrade() -> None:
    op.drop_index("ix_skill_categories_type", table_name="skill_categories")
    op.drop_table("skill_categories")
