"""add_admin_tables

Revision ID: add_admin_tables_001
Revises: add_auth_tables_001
Create Date: 2025-12-30

This migration adds admin module tables:
- admin_users: 管理员用户表
- subscription_plans: 订阅方案表
- system_configs: 系统配置表
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "add_admin_tables_001"
down_revision: Union[str, None] = "add_auth_tables_001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create admin_users table
    op.create_table(
        "admin_users",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("name", sa.String(100), nullable=True),
        sa.Column("role", sa.String(20), nullable=False, server_default="admin"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_admin_users_username", "admin_users", ["username"], unique=False)
    op.create_index("ix_admin_users_email", "admin_users", ["email"], unique=False)

    # Create subscription_plans table
    op.create_table(
        "subscription_plans",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("name_en", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("description_en", sa.Text(), nullable=True),
        sa.Column("price", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("currency", sa.String(10), nullable=False, server_default="'USD'"),
        sa.Column("billing_period", sa.String(20), nullable=False, server_default="'monthly'"),
        sa.Column("daily_quota", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("features", postgresql.ARRAY(sa.String()), nullable=False, server_default="{}"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_subscription_plans_is_active", "subscription_plans", ["is_active"], unique=False)
    op.create_index("ix_subscription_plans_sort_order", "subscription_plans", ["sort_order"], unique=False)

    # Create system_configs table
    op.create_table(
        "system_configs",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("key", sa.String(100), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(50), nullable=False, server_default="'general'"),
        sa.Column("is_sensitive", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("key"),
    )
    op.create_index("ix_system_configs_key", "system_configs", ["key"], unique=False)
    op.create_index("ix_system_configs_category", "system_configs", ["category"], unique=False)

    # Grant permissions to Supabase roles
    op.execute("GRANT ALL ON admin_users TO service_role")
    op.execute("GRANT ALL ON subscription_plans TO service_role")
    op.execute("GRANT ALL ON system_configs TO service_role")
    op.execute("GRANT SELECT ON subscription_plans TO authenticated")
    op.execute("GRANT SELECT ON system_configs TO authenticated")


def downgrade() -> None:
    # Drop system_configs table
    op.drop_index("ix_system_configs_category", table_name="system_configs")
    op.drop_index("ix_system_configs_key", table_name="system_configs")
    op.drop_table("system_configs")

    # Drop subscription_plans table
    op.drop_index("ix_subscription_plans_sort_order", table_name="subscription_plans")
    op.drop_index("ix_subscription_plans_is_active", table_name="subscription_plans")
    op.drop_table("subscription_plans")

    # Drop admin_users table
    op.drop_index("ix_admin_users_email", table_name="admin_users")
    op.drop_index("ix_admin_users_username", table_name="admin_users")
    op.drop_table("admin_users")
