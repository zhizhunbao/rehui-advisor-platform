"""merge_heads

Revision ID: ec1fe026126c
Revises: add_chat_tables_001, add_prompt_templates_fields_001
Create Date: 2025-12-30 14:39:54.014610

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec1fe026126c'
down_revision: Union[str, None] = ('add_chat_tables_001', 'add_prompt_templates_fields_001')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
