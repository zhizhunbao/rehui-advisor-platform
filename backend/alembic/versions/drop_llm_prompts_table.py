"""drop llm_prompts table

Revision ID: drop_llm_prompts
Revises: grant_llm_permissions
Create Date: 2025-01-01

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'drop_llm_prompts'
down_revision: Union[str, None] = 'grant_llm_permissions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 删除 llm_prompts 表（使用现有的 prompt_templates 表）
    op.execute("DROP TABLE IF EXISTS llm_prompts CASCADE")


def downgrade() -> None:
    # 重新创建 llm_prompts 表
    op.execute("""
        CREATE TABLE IF NOT EXISTS llm_prompts (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name VARCHAR(100) NOT NULL UNIQUE,
            display_name VARCHAR(200) NOT NULL,
            description TEXT,
            category VARCHAR(50) DEFAULT 'general',
            system_prompt TEXT NOT NULL,
            user_prompt_template TEXT,
            model_id UUID REFERENCES llm_models(id) ON DELETE SET NULL,
            temperature DECIMAL(3,2) DEFAULT 0.7,
            max_tokens INTEGER DEFAULT 2000,
            is_active BOOLEAN DEFAULT true,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
