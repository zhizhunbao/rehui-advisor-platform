"""disable llm rls for now

Revision ID: disable_llm_rls
Revises: add_llm_rls_policies
Create Date: 2025-01-01

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'disable_llm_rls'
down_revision: Union[str, None] = 'add_llm_rls_policies'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop all policies first
    op.execute("DROP POLICY IF EXISTS \"Allow service role full access on llm_models\" ON llm_models;")
    op.execute("DROP POLICY IF EXISTS \"Allow authenticated read on llm_models\" ON llm_models;")
    op.execute("DROP POLICY IF EXISTS \"Allow anon read active llm_models\" ON llm_models;")
    
    op.execute("DROP POLICY IF EXISTS \"Allow service role full access on llm_prompts\" ON llm_prompts;")
    op.execute("DROP POLICY IF EXISTS \"Allow authenticated read on llm_prompts\" ON llm_prompts;")
    op.execute("DROP POLICY IF EXISTS \"Allow anon read active llm_prompts\" ON llm_prompts;")
    
    # Disable RLS
    op.execute("ALTER TABLE llm_models DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE llm_prompts DISABLE ROW LEVEL SECURITY;")


def downgrade() -> None:
    # Re-enable RLS
    op.execute("ALTER TABLE llm_models ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE llm_prompts ENABLE ROW LEVEL SECURITY;")
