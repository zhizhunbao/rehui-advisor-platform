"""add_category_id_domain_id_to_data_sources

Revision ID: f5df662cab1c
Revises: 4f1ca7328b25
Create Date: 2025-12-31 22:19:18.788136

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5df662cab1c'
down_revision: Union[str, None] = '4f1ca7328b25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add category_id column with foreign key to domain_categories
    op.add_column(
        'data_sources',
        sa.Column('category_id', sa.UUID(), nullable=True)
    )
    op.create_foreign_key(
        'fk_data_sources_category_id',
        'data_sources',
        'domain_categories',
        ['category_id'],
        ['id'],
        ondelete='SET NULL'
    )
    
    # Add domain_id column with foreign key to domains
    op.add_column(
        'data_sources',
        sa.Column('domain_id', sa.UUID(), nullable=True)
    )
    op.create_foreign_key(
        'fk_data_sources_domain_id',
        'data_sources',
        'domains',
        ['domain_id'],
        ['id'],
        ondelete='SET NULL'
    )
    
    # Create indexes for better query performance
    op.create_index('idx_data_sources_category_id', 'data_sources', ['category_id'])
    op.create_index('idx_data_sources_domain_id', 'data_sources', ['domain_id'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_data_sources_domain_id', 'data_sources')
    op.drop_index('idx_data_sources_category_id', 'data_sources')
    
    # Drop foreign keys and columns
    op.drop_constraint('fk_data_sources_domain_id', 'data_sources', type_='foreignkey')
    op.drop_column('data_sources', 'domain_id')
    
    op.drop_constraint('fk_data_sources_category_id', 'data_sources', type_='foreignkey')
    op.drop_column('data_sources', 'category_id')
