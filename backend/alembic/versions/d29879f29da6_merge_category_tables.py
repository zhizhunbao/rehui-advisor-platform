"""merge_category_tables

Revision ID: d29879f29da6
Revises: add_github_links_permissions, add_prompt_categories_001
Create Date: 2025-12-30 18:23:08.225218

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd29879f29da6'
down_revision: Union[str, None] = ('add_github_links_permissions', 'add_prompt_categories_001')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
