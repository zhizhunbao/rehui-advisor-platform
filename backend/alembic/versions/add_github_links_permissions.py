"""add github_links permissions

Revision ID: add_github_links_permissions
Revises: add_github_links_table
Create Date: 2024-12-30
"""
from alembic import op

revision = 'add_github_links_permissions'
down_revision = 'add_github_links_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("GRANT ALL ON github_links TO service_role")
    op.execute("GRANT SELECT ON github_links TO authenticated")
    op.execute("GRANT SELECT ON github_links TO anon")


def downgrade() -> None:
    op.execute("REVOKE ALL ON github_links FROM service_role")
    op.execute("REVOKE SELECT ON github_links FROM authenticated")
    op.execute("REVOKE SELECT ON github_links FROM anon")
