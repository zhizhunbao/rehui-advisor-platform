"""add_template_en_to_prompt_templates

Revision ID: 4f1ca7328b25
Revises: 4d984873ef32
Create Date: 2025-01-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f1ca7328b25'
down_revision: Union[str, None] = '4d984873ef32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add template_en column for English version of prompts
    op.add_column(
        'prompt_templates',
        sa.Column('template_en', sa.Text(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('prompt_templates', 'template_en')
