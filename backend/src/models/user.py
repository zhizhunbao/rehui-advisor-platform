from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    password_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    location: Mapped[str | None] = mapped_column(String, nullable=True)
    budget: Mapped[float | None] = mapped_column(Float, nullable=True)
    risk_tolerance: Mapped[str | None] = mapped_column(String, nullable=True)

    # User type and quota
    user_type: Mapped[str] = mapped_column(String, default="ANONYMOUS")
    is_anonymous: Mapped[bool] = mapped_column(Boolean, default=True)
    session_token: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String, nullable=True)

    # Authentication fields (Requirements: 1.6, 1.7, 2.7, 3.3, 7.2, 9.3)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    email_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    oauth_provider: Mapped[str | None] = mapped_column(
        String, nullable=True
    )  # google, github
    oauth_provider_id: Mapped[str | None] = mapped_column(String, nullable=True)
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_login_ip: Mapped[str | None] = mapped_column(String, nullable=True)
    account_locked_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    deletion_requested_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Usage tracking
    search_count: Mapped[int] = mapped_column(Integer, default=0)
    search_limit: Mapped[int] = mapped_column(Integer, default=5)
    last_search_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    quota_reset_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Subscription
    subscription_status: Mapped[str | None] = mapped_column(String, nullable=True)
    subscription_tier: Mapped[str | None] = mapped_column(String, nullable=True)
    subscription_expiry: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        Index("ix_users_session_token", "session_token"),
        Index("ix_users_email", "email"),
        Index("ix_users_user_type", "user_type"),
        Index("ix_users_oauth_provider_id", "oauth_provider", "oauth_provider_id"),
    )
