"""add_prompt_categories_table

Revision ID: add_prompt_categories_001
Revises: add_skill_categories_001
Create Date: 2025-12-30

Create prompt_categories table for managing prompt category/source labels.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "add_prompt_categories_001"
down_revision: Union[str, None] = "add_skill_categories_001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create prompt_categories table
    op.create_table(
        "prompt_categories",
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
        sa.UniqueConstraint("type", "code", name="uq_prompt_categories_type_code"),
    )
    op.create_index("ix_prompt_categories_type", "prompt_categories", ["type"], unique=False)

    # Grant permissions
    op.execute("GRANT ALL ON prompt_categories TO service_role")
    op.execute("GRANT SELECT ON prompt_categories TO authenticated")
    op.execute("GRANT SELECT ON prompt_categories TO anon")

    # Insert initial category data
    op.execute("""
        INSERT INTO prompt_categories (type, code, label_zh, label_en, sort_order) VALUES
        ('category', 'roleplay', '角色扮演', 'Roleplay', 1),
        ('category', 'writing', '写作创作', 'Writing', 2),
        ('category', 'coding', '编程开发', 'Coding', 3),
        ('category', 'business', '商业营销', 'Business', 4),
        ('category', 'education', '教育学习', 'Education', 5),
        ('category', 'creative', '创意设计', 'Creative', 6),
        ('category', 'analysis', '分析研究', 'Analysis', 7),
        ('category', 'translation', '翻译语言', 'Translation', 8),
        ('category', 'assistant', '助手工具', 'Assistant', 9),
        ('category', 'system', '系统提示', 'System', 10),
        ('category', 'general', '通用', 'General', 99)
    """)

    # Insert initial source data
    op.execute("""
        INSERT INTO prompt_categories (type, code, label_zh, label_en, color, sort_order) VALUES
        ('source', 'awesome-chatgpt-prompts', 'ChatGPT Prompts', 'ChatGPT Prompts', 'green', 1),
        ('source', 'awesome-claude-prompts', 'Claude Prompts', 'Claude Prompts', 'blue', 2),
        ('source', 'awesome-system-prompts', 'System Prompts', 'System Prompts', 'violet', 3),
        ('source', 'ai-boost-prompts', 'AI Boost', 'AI Boost', 'cyan', 4),
        ('source', 'anthropic-official', 'Anthropic 官方', 'Anthropic Official', 'amber', 5)
    """)


def downgrade() -> None:
    op.drop_index("ix_prompt_categories_type", table_name="prompt_categories")
    op.drop_table("prompt_categories")
