from datetime import datetime
from typing import Any

from sqlalchemy import ARRAY, DateTime, Float, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, UUIDMixin


class Recommendation(Base, UUIDMixin):
    __tablename__ = "recommendations"

    user_id: Mapped[str] = mapped_column(String)
    domain: Mapped[str] = mapped_column(String)
    item_id: Mapped[str] = mapped_column(String)
    match_score: Mapped[float] = mapped_column(Float)
    ranking: Mapped[int] = mapped_column(Integer)
    pros: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    cons: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    reasoning: Mapped[str] = mapped_column(Text)
    alternative_ids: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_recommendations_user_domain", "user_id", "domain"),
        Index("ix_recommendations_match_score", "match_score"),
    )


class SearchHistory(Base, UUIDMixin):
    __tablename__ = "search_history"

    user_id: Mapped[str] = mapped_column(String)
    domain: Mapped[str] = mapped_column(String)
    parameters: Mapped[dict[str, Any]] = mapped_column(JSONB)
    result_count: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_search_history_user_id", "user_id"),
        Index("ix_search_history_domain", "domain"),
        Index("ix_search_history_created_at", "created_at"),
    )


class PriceHistory(Base, UUIDMixin):
    __tablename__ = "price_history"

    domain: Mapped[str] = mapped_column(String)
    item_id: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String, default="USD")
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_price_history_domain_item", "domain", "item_id"),
        Index("ix_price_history_timestamp", "timestamp"),
    )
