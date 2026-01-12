"""add retrieval engines permissions

Revision ID: add_retrieval_permissions
Revises: add_retrieval_engines
Create Date: 2024-12-31

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'add_retrieval_permissions'
down_revision: Union[str, None] = 'add_retrieval_engines'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 禁用 RLS（管理后台使用 service_role_key）
    op.execute("ALTER TABLE retrieval_engines DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE retrieval_domain_configs DISABLE ROW LEVEL SECURITY")
    
    # 授予权限
    op.execute("GRANT ALL ON retrieval_engines TO postgres, service_role")
    op.execute("GRANT ALL ON retrieval_domain_configs TO postgres, service_role")
    op.execute("GRANT SELECT ON retrieval_engines TO anon, authenticated")
    op.execute("GRANT SELECT ON retrieval_domain_configs TO anon, authenticated")


def downgrade() -> None:
    op.execute("REVOKE ALL ON retrieval_engines FROM postgres, service_role, anon, authenticated")
    op.execute("REVOKE ALL ON retrieval_domain_configs FROM postgres, service_role, anon, authenticated")
