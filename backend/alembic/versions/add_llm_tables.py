"""add llm tables

Revision ID: add_llm_tables
Revises: ec1fe026126c
Create Date: 2025-01-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'add_llm_tables'
down_revision: Union[str, None] = 'add_domain_categories_001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # LLM Models 表
    op.create_table(
        'llm_models',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False, comment='模型标识，如 gpt-4o, claude-3'),
        sa.Column('display_name', sa.String(100), nullable=False, comment='显示名称'),
        sa.Column('provider', sa.String(50), nullable=False, comment='提供商：openai, anthropic, google, deepseek'),
        sa.Column('api_endpoint', sa.Text(), nullable=False, comment='API 端点'),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('is_default', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('config', postgresql.JSONB(), server_default='{}', comment='模型配置：api_key, max_tokens 等'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('idx_llm_models_provider', 'llm_models', ['provider'])
    op.create_index('idx_llm_models_is_active', 'llm_models', ['is_active'])

    # LLM Prompts 表
    op.create_table(
        'llm_prompts',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False, unique=True, comment='Prompt 标识，如 resume_analysis'),
        sa.Column('display_name', sa.String(100), nullable=False, comment='显示名称'),
        sa.Column('description', sa.Text(), comment='描述'),
        sa.Column('category', sa.String(50), nullable=False, comment='分类：job, advisor, general'),
        sa.Column('system_prompt', sa.Text(), nullable=False, comment='系统提示词'),
        sa.Column('user_prompt_template', sa.Text(), comment='用户提示词模板，支持 {variable} 占位符'),
        sa.Column('model_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('llm_models.id', ondelete='SET NULL'), comment='指定模型，为空则使用默认'),
        sa.Column('temperature', sa.Numeric(2, 1), server_default='0.7', comment='温度参数'),
        sa.Column('max_tokens', sa.Integer(), server_default='2000', comment='最大 token 数'),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('idx_llm_prompts_category', 'llm_prompts', ['category'])
    op.create_index('idx_llm_prompts_is_active', 'llm_prompts', ['is_active'])


def downgrade() -> None:
    op.drop_table('llm_prompts')
    op.drop_table('llm_models')
