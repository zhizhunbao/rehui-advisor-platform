"""grant llm table permissions

Revision ID: grant_llm_permissions
Revises: disable_llm_rls
Create Date: 2025-01-01

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'grant_llm_permissions'
down_revision: Union[str, None] = 'disable_llm_rls'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Grant permissions to service_role
    op.execute("GRANT ALL ON llm_models TO service_role;")
    op.execute("GRANT ALL ON llm_prompts TO service_role;")
    
    # Grant permissions to authenticated users (read only)
    op.execute("GRANT SELECT ON llm_models TO authenticated;")
    op.execute("GRANT SELECT ON llm_prompts TO authenticated;")
    
    # Grant permissions to anon (read only)
    op.execute("GRANT SELECT ON llm_models TO anon;")
    op.execute("GRANT SELECT ON llm_prompts TO anon;")


def downgrade() -> None:
    op.execute("REVOKE ALL ON llm_models FROM service_role;")
    op.execute("REVOKE ALL ON llm_prompts FROM service_role;")
    op.execute("REVOKE SELECT ON llm_models FROM authenticated;")
    op.execute("REVOKE SELECT ON llm_prompts FROM authenticated;")
    op.execute("REVOKE SELECT ON llm_models FROM anon;")
    op.execute("REVOKE SELECT ON llm_prompts FROM anon;")
