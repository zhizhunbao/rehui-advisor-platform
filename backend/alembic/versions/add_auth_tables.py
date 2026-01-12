"""add_auth_tables

Revision ID: add_auth_tables_001
Revises: 890d75f54f33
Create Date: 2025-12-30

This migration adds authentication-related tables and fields:
- Extends users table with authentication fields
- Creates refresh_tokens table
- Creates password_reset_tokens table
- Creates login_attempts table
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "add_auth_tables_001"
down_revision: Union[str, None] = "890d75f54f33"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add authentication fields to users table
    # Requirements: 1.6, 1.7, 2.7, 3.3, 7.2, 9.3
    op.add_column(
        "users",
        sa.Column("email_verified", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "users",
        sa.Column("email_verified_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("oauth_provider", sa.String(), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("oauth_provider_id", sa.String(), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("last_login_ip", sa.String(), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("account_locked_until", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("deletion_requested_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Add index for OAuth provider lookup
    op.create_index(
        "ix_users_oauth_provider_id",
        "users",
        ["oauth_provider", "oauth_provider_id"],
        unique=False,
    )

    # Create refresh_tokens table
    # Requirements: 2.4, 4.4, 5.1
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("user_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("token_hash", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_revoked", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("device_info", sa.String(), nullable=True),
        sa.Column("ip_address", sa.String(), nullable=True),
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
    op.create_index("ix_refresh_tokens_user_id", "refresh_tokens", ["user_id"], unique=False)
    op.create_index(
        "ix_refresh_tokens_token_hash", "refresh_tokens", ["token_hash"], unique=False
    )
    op.create_index(
        "ix_refresh_tokens_expires_at", "refresh_tokens", ["expires_at"], unique=False
    )

    # Create password_reset_tokens table
    # Requirements: 6.1, 6.2, 6.3
    op.create_table(
        "password_reset_tokens",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("user_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("token_hash", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_used", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_password_reset_tokens_user_id",
        "password_reset_tokens",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_password_reset_tokens_token_hash",
        "password_reset_tokens",
        ["token_hash"],
        unique=False,
    )

    # Create login_attempts table
    # Requirements: 7.1, 7.2
    op.create_table(
        "login_attempts",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("ip_address", sa.String(), nullable=False),
        sa.Column("success", sa.Boolean(), nullable=False),
        sa.Column(
            "attempted_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_login_attempts_email", "login_attempts", ["email"], unique=False)
    op.create_index(
        "ix_login_attempts_ip_address", "login_attempts", ["ip_address"], unique=False
    )
    op.create_index(
        "ix_login_attempts_attempted_at", "login_attempts", ["attempted_at"], unique=False
    )
    op.create_index(
        "ix_login_attempts_email_ip",
        "login_attempts",
        ["email", "ip_address"],
        unique=False,
    )

    # Grant permissions to Supabase roles
    op.execute("GRANT ALL ON refresh_tokens TO service_role")
    op.execute("GRANT ALL ON password_reset_tokens TO service_role")
    op.execute("GRANT ALL ON login_attempts TO service_role")


def downgrade() -> None:
    # Drop login_attempts table
    op.drop_index("ix_login_attempts_email_ip", table_name="login_attempts")
    op.drop_index("ix_login_attempts_attempted_at", table_name="login_attempts")
    op.drop_index("ix_login_attempts_ip_address", table_name="login_attempts")
    op.drop_index("ix_login_attempts_email", table_name="login_attempts")
    op.drop_table("login_attempts")

    # Drop password_reset_tokens table
    op.drop_index(
        "ix_password_reset_tokens_token_hash", table_name="password_reset_tokens"
    )
    op.drop_index("ix_password_reset_tokens_user_id", table_name="password_reset_tokens")
    op.drop_table("password_reset_tokens")

    # Drop refresh_tokens table
    op.drop_index("ix_refresh_tokens_expires_at", table_name="refresh_tokens")
    op.drop_index("ix_refresh_tokens_token_hash", table_name="refresh_tokens")
    op.drop_index("ix_refresh_tokens_user_id", table_name="refresh_tokens")
    op.drop_table("refresh_tokens")

    # Remove authentication fields from users table
    op.drop_index("ix_users_oauth_provider_id", table_name="users")
    op.drop_column("users", "deletion_requested_at")
    op.drop_column("users", "account_locked_until")
    op.drop_column("users", "last_login_ip")
    op.drop_column("users", "last_login_at")
    op.drop_column("users", "oauth_provider_id")
    op.drop_column("users", "oauth_provider")
    op.drop_column("users", "email_verified_at")
    op.drop_column("users", "email_verified")
