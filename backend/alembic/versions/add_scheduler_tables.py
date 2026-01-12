"""add scheduler tables

Revision ID: add_scheduler_tables
Revises: add_retrieval_permissions
Create Date: 2024-12-31

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = 'add_scheduler_tables'
down_revision: Union[str, None] = 'add_retrieval_permissions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 调度任务表
    op.create_table(
        'scheduled_jobs',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False, comment='任务名称'),
        sa.Column('description', sa.Text(), comment='任务描述'),
        sa.Column('job_type', sa.String(50), nullable=False, comment='任务类型'),
        sa.Column('cron_expression', sa.String(100), nullable=False, comment='Cron 表达式'),
        sa.Column('parameters', postgresql.JSONB(), server_default='{}', comment='任务参数'),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False, comment='是否启用'),
        sa.Column('last_run_at', sa.DateTime(timezone=True), comment='上次执行时间'),
        sa.Column('next_run_at', sa.DateTime(timezone=True), comment='下次执行时间'),
        sa.Column('last_status', sa.String(20), comment='上次执行状态'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('idx_scheduled_jobs_type', 'scheduled_jobs', ['job_type'])
    op.create_index('idx_scheduled_jobs_active', 'scheduled_jobs', ['is_active'])

    # 任务执行记录表
    op.create_table(
        'job_executions',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('job_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scheduled_jobs.id', ondelete='CASCADE'), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False, comment='开始时间'),
        sa.Column('finished_at', sa.DateTime(timezone=True), comment='结束时间'),
        sa.Column('status', sa.String(20), nullable=False, comment='执行状态: running, success, failed'),
        sa.Column('result', postgresql.JSONB(), comment='执行结果'),
        sa.Column('error_message', sa.Text(), comment='错误信息'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('idx_job_executions_job_id', 'job_executions', ['job_id'])
    op.create_index('idx_job_executions_status', 'job_executions', ['status'])
    op.create_index('idx_job_executions_started_at', 'job_executions', ['started_at'])

    # 更新时间触发器
    op.execute("""
        CREATE OR REPLACE FUNCTION update_scheduler_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER trigger_scheduled_jobs_updated_at
            BEFORE UPDATE ON scheduled_jobs
            FOR EACH ROW EXECUTE FUNCTION update_scheduler_updated_at();
    """)

    # 禁用 RLS（管理后台使用 service_role_key）
    op.execute("ALTER TABLE scheduled_jobs DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE job_executions DISABLE ROW LEVEL SECURITY")

    # 授予权限
    op.execute("GRANT ALL ON scheduled_jobs TO postgres, service_role")
    op.execute("GRANT ALL ON job_executions TO postgres, service_role")


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trigger_scheduled_jobs_updated_at ON scheduled_jobs")
    op.execute("DROP FUNCTION IF EXISTS update_scheduler_updated_at()")
    op.drop_table('job_executions')
    op.drop_table('scheduled_jobs')
