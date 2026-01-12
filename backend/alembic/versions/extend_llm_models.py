"""extend llm_models with region, version, pricing

Revision ID: extend_llm_models
Revises: drop_llm_prompts
Create Date: 2025-01-01

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'extend_llm_models'
down_revision: Union[str, None] = 'drop_llm_prompts'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 添加新字段
    op.execute("""
        ALTER TABLE llm_models
        ADD COLUMN IF NOT EXISTS region VARCHAR(20) DEFAULT 'global',
        ADD COLUMN IF NOT EXISTS version VARCHAR(50),
        ADD COLUMN IF NOT EXISTS category VARCHAR(50) DEFAULT 'general',
        ADD COLUMN IF NOT EXISTS deployment_type VARCHAR(20) DEFAULT 'api',
        ADD COLUMN IF NOT EXISTS input_price DECIMAL(10,6) DEFAULT 0,
        ADD COLUMN IF NOT EXISTS output_price DECIMAL(10,6) DEFAULT 0,
        ADD COLUMN IF NOT EXISTS is_free BOOLEAN DEFAULT false,
        ADD COLUMN IF NOT EXISTS context_window INTEGER DEFAULT 4096,
        ADD COLUMN IF NOT EXISTS max_output_tokens INTEGER DEFAULT 4096,
        ADD COLUMN IF NOT EXISTS capabilities JSONB DEFAULT '[]'::jsonb,
        ADD COLUMN IF NOT EXISTS description TEXT,
        ADD COLUMN IF NOT EXISTS docker_image VARCHAR(255),
        ADD COLUMN IF NOT EXISTS hardware_requirements JSONB DEFAULT '{}'::jsonb,
        ADD COLUMN IF NOT EXISTS rate_limit JSONB DEFAULT '{}'::jsonb,
        ADD COLUMN IF NOT EXISTS latency_ms INTEGER,
        ADD COLUMN IF NOT EXISTS quality_score DECIMAL(3,1),
        ADD COLUMN IF NOT EXISTS license VARCHAR(50),
        ADD COLUMN IF NOT EXISTS release_date DATE,
        ADD COLUMN IF NOT EXISTS is_deprecated BOOLEAN DEFAULT false,
        ADD COLUMN IF NOT EXISTS fallback_model_id UUID REFERENCES llm_models(id) ON DELETE SET NULL,
        ADD COLUMN IF NOT EXISTS sort_order INTEGER DEFAULT 0
    """)
    
    # 添加注释
    op.execute("COMMENT ON COLUMN llm_models.region IS '区域: us, cn, eu, global'")
    op.execute("COMMENT ON COLUMN llm_models.version IS '模型版本号'")
    op.execute("COMMENT ON COLUMN llm_models.category IS '适用场景: general, chat, coding, reasoning, vision, embedding'")
    op.execute("COMMENT ON COLUMN llm_models.deployment_type IS '部署类型: api(调用API), local(本地部署), hybrid(混合)'")
    op.execute("COMMENT ON COLUMN llm_models.input_price IS '输入价格 ($/1M tokens)'")
    op.execute("COMMENT ON COLUMN llm_models.output_price IS '输出价格 ($/1M tokens)'")
    op.execute("COMMENT ON COLUMN llm_models.is_free IS '是否免费'")
    op.execute("COMMENT ON COLUMN llm_models.context_window IS '上下文窗口大小'")
    op.execute("COMMENT ON COLUMN llm_models.max_output_tokens IS '最大输出 token 数'")
    op.execute("COMMENT ON COLUMN llm_models.capabilities IS '能力标签: vision, function_calling, json_mode 等'")
    op.execute("COMMENT ON COLUMN llm_models.docker_image IS '本地部署的 Docker 镜像'")
    op.execute("COMMENT ON COLUMN llm_models.hardware_requirements IS '硬件要求: {gpu, vram, ram}'")
    op.execute("COMMENT ON COLUMN llm_models.rate_limit IS '速率限制: {rpm, tpm}'")
    op.execute("COMMENT ON COLUMN llm_models.latency_ms IS '平均响应延迟(毫秒)'")
    op.execute("COMMENT ON COLUMN llm_models.quality_score IS '质量评分(1-10)'")
    op.execute("COMMENT ON COLUMN llm_models.license IS '开源协议: MIT, Apache, Commercial 等'")
    op.execute("COMMENT ON COLUMN llm_models.release_date IS '模型发布日期'")
    op.execute("COMMENT ON COLUMN llm_models.is_deprecated IS '是否已弃用'")
    op.execute("COMMENT ON COLUMN llm_models.fallback_model_id IS '备用模型ID'")


def downgrade() -> None:
    op.execute("""
        ALTER TABLE llm_models
        DROP COLUMN IF EXISTS region,
        DROP COLUMN IF EXISTS version,
        DROP COLUMN IF EXISTS category,
        DROP COLUMN IF EXISTS deployment_type,
        DROP COLUMN IF EXISTS input_price,
        DROP COLUMN IF EXISTS output_price,
        DROP COLUMN IF EXISTS is_free,
        DROP COLUMN IF EXISTS context_window,
        DROP COLUMN IF EXISTS max_output_tokens,
        DROP COLUMN IF EXISTS capabilities,
        DROP COLUMN IF EXISTS description,
        DROP COLUMN IF EXISTS docker_image,
        DROP COLUMN IF EXISTS hardware_requirements,
        DROP COLUMN IF EXISTS rate_limit,
        DROP COLUMN IF EXISTS latency_ms,
        DROP COLUMN IF EXISTS quality_score,
        DROP COLUMN IF EXISTS license,
        DROP COLUMN IF EXISTS release_date,
        DROP COLUMN IF EXISTS is_deprecated,
        DROP COLUMN IF EXISTS fallback_model_id,
        DROP COLUMN IF EXISTS sort_order
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE llm_models
        DROP COLUMN IF EXISTS region,
        DROP COLUMN IF EXISTS version,
        DROP COLUMN IF EXISTS category,
        DROP COLUMN IF EXISTS input_price,
        DROP COLUMN IF EXISTS output_price,
        DROP COLUMN IF EXISTS context_window,
        DROP COLUMN IF EXISTS max_output_tokens,
        DROP COLUMN IF EXISTS capabilities,
        DROP COLUMN IF EXISTS description,
        DROP COLUMN IF EXISTS sort_order
    """)
