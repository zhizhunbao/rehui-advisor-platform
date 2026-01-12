"""merge_discovery_keywords

Revision ID: cc76d2e96477
Revises: add_discovery_keywords, add_system_logs_table
Create Date: 2025-12-31 20:52:51.432850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc76d2e96477'
down_revision: Union[str, None] = ('add_discovery_keywords', 'add_system_logs_table')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
