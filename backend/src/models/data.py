from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, Index, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, UUIDMixin


class RawData(Base, UUIDMixin):
    __tablename__ = "raw_data"

    domain: Mapped[str] = mapped_column(String)
    source: Mapped[str] = mapped_column(String)
    url: Mapped[str | None] = mapped_column(String, nullable=True)
    content: Mapped[dict[str, Any]] = mapped_column(JSONB)
    status: Mapped[str] = mapped_column(String, default="PENDING")
    scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    user_id: Mapped[str | None] = mapped_column(String, nullable=True)

    __table_args__ = (
        Index("ix_raw_data_domain", "domain"),
        Index("ix_raw_data_status", "status"),
        Index("ix_raw_data_scraped_at", "scraped_at"),
    )


class CleanedData(Base, UUIDMixin):
    __tablename__ = "cleaned_data"

    domain: Mapped[str] = mapped_column(String)
    raw_data_id: Mapped[str] = mapped_column(String)
    normalized_content: Mapped[dict[str, Any]] = mapped_column(JSONB)
    quality: Mapped[float] = mapped_column(Float, default=0.0)
    processed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    user_id: Mapped[str | None] = mapped_column(String, nullable=True)

    __table_args__ = (
        Index("ix_cleaned_data_domain", "domain"),
        Index("ix_cleaned_data_quality", "quality"),
    )


class AnalysisResult(Base, UUIDMixin):
    __tablename__ = "analysis_results"

    domain: Mapped[str] = mapped_column(String)
    cleaned_data_id: Mapped[str] = mapped_column(String)
    metrics: Mapped[dict[str, Any]] = mapped_column(JSONB)
    insights: Mapped[dict[str, Any]] = mapped_column(JSONB)
    trends: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    analyzed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_analysis_results_domain", "domain"),
        Index("ix_analysis_results_analyzed_at", "analyzed_at"),
    )
