from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, TimestampMixin, UUIDMixin


class Domain(Base, UUIDMixin, TimestampMixin):
    """领域配置"""

    __tablename__ = "domains"

    code: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    name_en: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    icon: Mapped[str] = mapped_column(String(50), default="Plane")
    color: Mapped[str] = mapped_column(String(50), default="bg-blue-500")
    prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    prompt_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (
        Index("ix_domains_code", "code"),
        Index("ix_domains_is_active", "is_active"),
    )


class PromptTemplate(Base, UUIDMixin, TimestampMixin):
    """Prompt 模板"""

    __tablename__ = "prompt_templates"

    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text)
    content_en: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(50), default="general")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    __table_args__ = (Index("ix_prompt_templates_category", "category"),)


class Question(Base, UUIDMixin, TimestampMixin):
    """问题库"""

    __tablename__ = "questions"

    domain_id: Mapped[str] = mapped_column(String(36), ForeignKey("domains.id"))
    text: Mapped[str] = mapped_column(Text)
    text_en: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(String(20), default="single")  # single, multiple, text
    options: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    __table_args__ = (Index("ix_questions_domain_id", "domain_id"),)


class CrawlSource(Base, UUIDMixin, TimestampMixin):
    """数据抓取源"""

    __tablename__ = "crawl_sources"

    name: Mapped[str] = mapped_column(String(100))
    url: Mapped[str] = mapped_column(String(500))
    domain_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("domains.id"), nullable=True)
    schedule: Mapped[str | None] = mapped_column(String(50), nullable=True)  # cron expression
    config: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_status: Mapped[str | None] = mapped_column(String(20), nullable=True)


class CrawlTask(Base, UUIDMixin, TimestampMixin):
    """抓取任务记录"""

    __tablename__ = "crawl_tasks"

    source_id: Mapped[str] = mapped_column(String(36), ForeignKey("crawl_sources.id"))
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, running, success, failed
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    records_count: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (Index("ix_crawl_tasks_source_id", "source_id"),)
