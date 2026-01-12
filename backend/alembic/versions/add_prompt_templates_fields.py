"""add_prompt_templates_fields

Revision ID: add_prompt_templates_fields_001
Revises: add_admin_content_001
Create Date: 2025-12-30

Add category, source, repo fields to prompt_templates table for Claude Skills.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "add_prompt_templates_fields_001"
down_revision: Union[str, None] = "add_admin_content_001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add category column
    op.add_column(
        "prompt_templates",
        sa.Column("category", sa.String(50), nullable=True, server_default="'tool'"),
    )
    
    # Add source column (official/community)
    op.add_column(
        "prompt_templates",
        sa.Column("source", sa.String(50), nullable=True, server_default="'official'"),
    )
    
    # Add repo column (GitHub repo path)
    op.add_column(
        "prompt_templates",
        sa.Column("repo", sa.String(200), nullable=True),
    )
    
    # Create indexes
    op.create_index("ix_prompt_templates_category", "prompt_templates", ["category"], unique=False)
    op.create_index("ix_prompt_templates_source", "prompt_templates", ["source"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_prompt_templates_source", table_name="prompt_templates")
    op.drop_index("ix_prompt_templates_category", table_name="prompt_templates")
    op.drop_column("prompt_templates", "repo")
    op.drop_column("prompt_templates", "source")
    op.drop_column("prompt_templates", "category")
