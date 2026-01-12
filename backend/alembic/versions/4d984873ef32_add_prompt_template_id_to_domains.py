"""add_prompt_template_id_to_domains

Revision ID: 4d984873ef32
Revises: 
Create Date: 2025-01-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d984873ef32'
down_revision: Union[str, None] = 'cc76d2e96477'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add prompt_template_id foreign key column to domains table
    op.add_column(
        'domains',
        sa.Column('prompt_template_id', sa.UUID(), nullable=True)
    )
    
    # Create foreign key constraint
    op.create_foreign_key(
        'fk_domains_prompt_template_id',
        'domains',
        'prompt_templates',
        ['prompt_template_id'],
        ['id'],
        ondelete='SET NULL'
    )
    
    # Create index for better query performance
    op.create_index(
        'idx_domains_prompt_template_id',
        'domains',
        ['prompt_template_id']
    )


def downgrade() -> None:
    # Drop index
    op.drop_index('idx_domains_prompt_template_id', table_name='domains')
    
    # Drop foreign key constraint
    op.drop_constraint('fk_domains_prompt_template_id', 'domains', type_='foreignkey')
    
    # Drop column
    op.drop_column('domains', 'prompt_template_id')
