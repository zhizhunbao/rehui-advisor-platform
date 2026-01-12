"""Authentication related models for user authentication system.

This module contains models for:
- RefreshToken: JWT refresh token storage with rotation support
- PasswordResetToken: Password reset link tokens
- LoginAttempt: Login attempt tracking for security
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, TimestampMixin, UUIDMixin


class RefreshToken(Base, UUIDMixin, TimestampMixin):
    """Refresh token model for JWT token rotation.

    Requirements: 2.4, 4.4, 5.1
    - Stores hashed refresh tokens (not plaintext)
    - Supports token rotation by tracking revocation
    - Tracks device and IP for security
    """

    __tablename__ = "refresh_tokens"

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False)
    token_hash: Mapped[str] = mapped_column(String, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    device_info: Mapped[str | None] = mapped_column(String, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String, nullable=True)

    __table_args__ = (
        Index("ix_refresh_tokens_user_id", "user_id"),
        Index("ix_refresh_tokens_token_hash", "token_hash"),
        Index("ix_refresh_tokens_expires_at", "expires_at"),
    )


class PasswordResetToken(Base, UUIDMixin):
    """Password reset token model.

    Requirements: 6.1, 6.2, 6.3
    - Stores hashed reset tokens
    - Tracks expiration (1 hour)
    - Single-use enforcement via is_used flag
    """

    __tablename__ = "password_reset_tokens"

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False)
    token_hash: Mapped[str] = mapped_column(String, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default="now()"
    )

    __table_args__ = (
        Index("ix_password_reset_tokens_user_id", "user_id"),
        Index("ix_password_reset_tokens_token_hash", "token_hash"),
    )


class LoginAttempt(Base, UUIDMixin):
    """Login attempt tracking for security.

    Requirements: 7.1, 7.2
    - Tracks failed login attempts by email and IP
    - Used for rate limiting and account lockout
    """

    __tablename__ = "login_attempts"

    email: Mapped[str] = mapped_column(String, nullable=False)
    ip_address: Mapped[str] = mapped_column(String, nullable=False)
    success: Mapped[bool] = mapped_column(Boolean, nullable=False)
    attempted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default="now()"
    )

    __table_args__ = (
        Index("ix_login_attempts_email", "email"),
        Index("ix_login_attempts_ip_address", "ip_address"),
        Index("ix_login_attempts_attempted_at", "attempted_at"),
        Index("ix_login_attempts_email_ip", "email", "ip_address"),
    )
