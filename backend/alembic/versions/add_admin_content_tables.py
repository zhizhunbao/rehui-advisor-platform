"""add_admin_content_tables

Revision ID: add_admin_content_001
Revises: add_admin_tables_001
Create Date: 2025-12-30

This migration adds admin content management tables:
- domains: 领域配置表
- prompt_templates: 提示词模板表
- questions: 问题配置表
- crawl_sources: 爬虫源配置表
- crawl_tasks: 爬虫任务表
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "add_admin_content_001"
down_revision: Union[str, None] = "add_admin_tables_001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create domains table
    op.create_table(
        "domains",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("name_en", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("description_en", sa.Text(), nullable=True),
        sa.Column("icon", sa.String(50), nullable=True),
        sa.Column("color", sa.String(20), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("name_en"),
    )
    op.create_index("ix_domains_is_active", "domains", ["is_active"], unique=False)
    op.create_index("ix_domains_sort_order", "domains", ["sort_order"], unique=False)

    # Create prompt_templates table
    op.create_table(
        "prompt_templates",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("domain_id", sa.UUID(as_uuid=False), nullable=True),
        sa.Column("template", sa.Text(), nullable=False),
        sa.Column("variables", postgresql.ARRAY(sa.String()), nullable=False, server_default="{}"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("ix_prompt_templates_domain_id", "prompt_templates", ["domain_id"], unique=False)
    op.create_index("ix_prompt_templates_is_active", "prompt_templates", ["is_active"], unique=False)

    # Create questions table
    op.create_table(
        "questions",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("domain_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("question_en", sa.Text(), nullable=False),
        sa.Column("field_name", sa.String(100), nullable=False),
        sa.Column("field_type", sa.String(50), nullable=False, server_default="'text'"),
        sa.Column("options", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("validation", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("is_required", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_questions_domain_id", "questions", ["domain_id"], unique=False)
    op.create_index("ix_questions_sort_order", "questions", ["sort_order"], unique=False)

    # Create crawl_sources table
    op.create_table(
        "crawl_sources",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("domain_id", sa.UUID(as_uuid=False), nullable=True),
        sa.Column("url", sa.String(500), nullable=False),
        sa.Column("source_type", sa.String(50), nullable=False, server_default="'web'"),
        sa.Column("config", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("schedule", sa.String(100), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("last_crawled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_crawl_sources_domain_id", "crawl_sources", ["domain_id"], unique=False)
    op.create_index("ix_crawl_sources_is_active", "crawl_sources", ["is_active"], unique=False)

    # Create crawl_tasks table
    op.create_table(
        "crawl_tasks",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("source_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="'pending'"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("items_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_crawl_tasks_source_id", "crawl_tasks", ["source_id"], unique=False)
    op.create_index("ix_crawl_tasks_status", "crawl_tasks", ["status"], unique=False)

    # Grant permissions to Supabase roles
    tables = ["domains", "prompt_templates", "questions", "crawl_sources", "crawl_tasks"]
    for table in tables:
        op.execute(f"GRANT ALL ON {table} TO service_role")
    
    # Grant read access to authenticated users for domains
    op.execute("GRANT SELECT ON domains TO authenticated")
    op.execute("GRANT SELECT ON domains TO anon")


def downgrade() -> None:
    op.drop_index("ix_crawl_tasks_status", table_name="crawl_tasks")
    op.drop_index("ix_crawl_tasks_source_id", table_name="crawl_tasks")
    op.drop_table("crawl_tasks")

    op.drop_index("ix_crawl_sources_is_active", table_name="crawl_sources")
    op.drop_index("ix_crawl_sources_domain_id", table_name="crawl_sources")
    op.drop_table("crawl_sources")

    op.drop_index("ix_questions_sort_order", table_name="questions")
    op.drop_index("ix_questions_domain_id", table_name="questions")
    op.drop_table("questions")

    op.drop_index("ix_prompt_templates_is_active", table_name="prompt_templates")
    op.drop_index("ix_prompt_templates_domain_id", table_name="prompt_templates")
    op.drop_table("prompt_templates")

    op.drop_index("ix_domains_sort_order", table_name="domains")
    op.drop_index("ix_domains_is_active", table_name="domains")
    op.drop_table("domains")
