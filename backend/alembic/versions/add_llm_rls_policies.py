"""add llm rls policies

Revision ID: add_llm_rls_policies
Revises: add_llm_tables
Create Date: 2025-01-01

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'add_llm_rls_policies'
down_revision: Union[str, None] = 'add_llm_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable RLS
    op.execute("ALTER TABLE llm_models ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE llm_prompts ENABLE ROW LEVEL SECURITY;")
    
    # llm_models policies
    op.execute("""
        CREATE POLICY "Allow service role full access on llm_models"
        ON llm_models
        FOR ALL
        TO service_role
        USING (true)
        WITH CHECK (true);
    """)
    
    op.execute("""
        CREATE POLICY "Allow authenticated read on llm_models"
        ON llm_models
        FOR SELECT
        TO authenticated
        USING (is_active = true);
    """)
    
    op.execute("""
        CREATE POLICY "Allow anon read active llm_models"
        ON llm_models
        FOR SELECT
        TO anon
        USING (is_active = true);
    """)
    
    # llm_prompts policies
    op.execute("""
        CREATE POLICY "Allow service role full access on llm_prompts"
        ON llm_prompts
        FOR ALL
        TO service_role
        USING (true)
        WITH CHECK (true);
    """)
    
    op.execute("""
        CREATE POLICY "Allow authenticated read on llm_prompts"
        ON llm_prompts
        FOR SELECT
        TO authenticated
        USING (is_active = true);
    """)
    
    op.execute("""
        CREATE POLICY "Allow anon read active llm_prompts"
        ON llm_prompts
        FOR SELECT
        TO anon
        USING (is_active = true);
    """)


def downgrade() -> None:
    # Drop policies
    op.execute("DROP POLICY IF EXISTS \"Allow service role full access on llm_models\" ON llm_models;")
    op.execute("DROP POLICY IF EXISTS \"Allow authenticated read on llm_models\" ON llm_models;")
    op.execute("DROP POLICY IF EXISTS \"Allow anon read active llm_models\" ON llm_models;")
    
    op.execute("DROP POLICY IF EXISTS \"Allow service role full access on llm_prompts\" ON llm_prompts;")
    op.execute("DROP POLICY IF EXISTS \"Allow authenticated read on llm_prompts\" ON llm_prompts;")
    op.execute("DROP POLICY IF EXISTS \"Allow anon read active llm_prompts\" ON llm_prompts;")
    
    # Disable RLS
    op.execute("ALTER TABLE llm_models DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE llm_prompts DISABLE ROW LEVEL SECURITY;")
