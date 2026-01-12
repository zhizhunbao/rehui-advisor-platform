from datetime import datetime
from typing import Any

from sqlalchemy import ARRAY, Boolean, DateTime, Float, Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, TimestampMixin, UUIDMixin


class InsuranceProduct(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "insurance_products"

    provider: Mapped[str] = mapped_column(String)
    product_name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    premium: Mapped[float] = mapped_column(Float)
    deductible: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String, default="USD")
    payment_frequency: Mapped[str] = mapped_column(String)
    coverage_limit: Mapped[float] = mapped_column(Float)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    customer_satisfaction: Mapped[float | None] = mapped_column(Float, nullable=True)
    features: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    exclusions: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    discount_types: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    coverage_details: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    eligibility_criteria: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    source: Mapped[str] = mapped_column(String)
    scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        Index("ix_insurance_products_type", "type"),
        Index("ix_insurance_products_provider", "provider"),
        Index("ix_insurance_products_premium", "premium"),
        Index("ix_insurance_products_valid_until", "valid_until"),
    )


class InsuranceQuote(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "insurance_quotes"

    user_id: Mapped[str | None] = mapped_column(String, nullable=True)
    session_token: Mapped[str | None] = mapped_column(String, nullable=True)
    insurance_type: Mapped[str] = mapped_column(String)
    request_data: Mapped[dict[str, Any]] = mapped_column(JSONB)
    zip_code: Mapped[str] = mapped_column(String)
    quotes: Mapped[dict[str, Any]] = mapped_column(JSONB)
    comparison_result: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String, default="ACTIVE")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    product_id: Mapped[str | None] = mapped_column(String, nullable=True)

    __table_args__ = (
        Index("ix_insurance_quotes_user_id", "user_id"),
        Index("ix_insurance_quotes_session_token", "session_token"),
        Index("ix_insurance_quotes_type", "insurance_type"),
        Index("ix_insurance_quotes_zip_code", "zip_code"),
        Index("ix_insurance_quotes_status", "status"),
        Index("ix_insurance_quotes_expires_at", "expires_at"),
    )


class InsuranceProvider(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "insurance_providers"

    name: Mapped[str] = mapped_column(String, unique=True)
    code: Mapped[str] = mapped_column(String, unique=True)
    logo: Mapped[str | None] = mapped_column(String, nullable=True)
    website: Mapped[str | None] = mapped_column(String, nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String, nullable=True)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    customer_satisfaction: Mapped[float | None] = mapped_column(Float, nullable=True)
    supported_types: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    license_states: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    am_best_rating: Mapped[str | None] = mapped_column(String, nullable=True)
    features: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    discount_programs: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    claims_phone: Mapped[str | None] = mapped_column(String, nullable=True)
    customer_service_hours: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    __table_args__ = (
        Index("ix_insurance_providers_code", "code"),
        Index("ix_insurance_providers_rating", "rating"),
    )


class InsuranceClaim(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "insurance_claims"

    user_id: Mapped[str] = mapped_column(String)
    insurance_type: Mapped[str] = mapped_column(String)
    provider: Mapped[str] = mapped_column(String)
    claim_number: Mapped[str | None] = mapped_column(String, nullable=True)
    incident_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    reported_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    claim_type: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    damage_amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    settled_amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String, default="PENDING")
    resolution: Mapped[str | None] = mapped_column(Text, nullable=True)
    documents: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    photos: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)

    __table_args__ = (
        Index("ix_insurance_claims_user_id", "user_id"),
        Index("ix_insurance_claims_type", "insurance_type"),
        Index("ix_insurance_claims_status", "status"),
        Index("ix_insurance_claims_incident_date", "incident_date"),
    )
