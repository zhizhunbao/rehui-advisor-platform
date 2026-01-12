"""drop region column from llm_models

Revision ID: drop_llm_region
Revises: extend_llm_models
Create Date: 2025-01-01

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'drop_llm_region'
down_revision: Union[str, None] = 'extend_llm_models'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE llm_models DROP COLUMN IF EXISTS region")


def downgrade() -> None:
    op.execute("ALTER TABLE llm_models ADD COLUMN IF NOT EXISTS region VARCHAR(20) DEFAULT 'global'")
    op.execute("COMMENT ON COLUMN llm_models.region IS '区域: us, cn, eu, global'")
