"""remove_old_category_subcategory_columns

Revision ID: c376f7f4b087
Revises: f5df662cab1c
Create Date: 2025-12-31 22:31:31.777533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c376f7f4b087'
down_revision: Union[str, None] = 'f5df662cab1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop old category and subcategory string columns
    op.drop_column('data_sources', 'category')
    op.drop_column('data_sources', 'subcategory')


def downgrade() -> None:
    # Re-add old columns if needed
    op.add_column('data_sources', sa.Column('category', sa.String(), nullable=True))
    op.add_column('data_sources', sa.Column('subcategory', sa.String(), nullable=True))
