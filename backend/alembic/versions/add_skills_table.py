"""add_skills_table

Revision ID: add_skills_table_001
Revises: ec1fe026126c
Create Date: 2025-12-30

Create skills table for Claude Skills management.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "add_skills_table_001"
down_revision: Union[str, None] = "ec1fe026126c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create skills table
    op.create_table(
        "skills",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(50), nullable=False, server_default="'tool'"),
        sa.Column("source", sa.String(50), nullable=False, server_default="'official'"),
        sa.Column("repo", sa.String(200), nullable=True),
        sa.Column("content", sa.Text(), nullable=True),
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
    op.create_index("ix_skills_category", "skills", ["category"], unique=False)
    op.create_index("ix_skills_source", "skills", ["source"], unique=False)
    op.create_index("ix_skills_is_active", "skills", ["is_active"], unique=False)

    # Grant permissions
    op.execute("GRANT ALL ON skills TO service_role")
    op.execute("GRANT SELECT ON skills TO authenticated")
    op.execute("GRANT SELECT ON skills TO anon")

    # Remove category, source, repo from prompt_templates (revert to original)
    op.drop_index("ix_prompt_templates_source", table_name="prompt_templates")
    op.drop_index("ix_prompt_templates_category", table_name="prompt_templates")
    op.drop_column("prompt_templates", "repo")
    op.drop_column("prompt_templates", "source")
    op.drop_column("prompt_templates", "category")


def downgrade() -> None:
    # Add back columns to prompt_templates
    op.add_column(
        "prompt_templates",
        sa.Column("category", sa.String(50), nullable=True, server_default="'tool'"),
    )
    op.add_column(
        "prompt_templates",
        sa.Column("source", sa.String(50), nullable=True, server_default="'official'"),
    )
    op.add_column(
        "prompt_templates",
        sa.Column("repo", sa.String(200), nullable=True),
    )
    op.create_index("ix_prompt_templates_category", "prompt_templates", ["category"], unique=False)
    op.create_index("ix_prompt_templates_source", "prompt_templates", ["source"], unique=False)

    # Drop skills table
    op.drop_index("ix_skills_is_active", table_name="skills")
    op.drop_index("ix_skills_source", table_name="skills")
    op.drop_index("ix_skills_category", table_name="skills")
    op.drop_table("skills")
