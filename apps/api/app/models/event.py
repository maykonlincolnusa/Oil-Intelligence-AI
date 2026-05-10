from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import OilImpact, RiskLevel


class NewsArticle(Base, TimestampMixin):
    __tablename__ = "news_articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300), index=True)
    summary: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(String(500), unique=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    source: Mapped[str] = mapped_column(String(120))
    language: Mapped[str] = mapped_column(String(10), default="en")
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)

    events: Mapped[list["GeopoliticalEvent"]] = relationship(back_populates="article")


class GeopoliticalEvent(Base, TimestampMixin):
    __tablename__ = "geopolitical_events"
    __table_args__ = (
        Index("ix_geopolitical_events_event_time", "event_time"),
        Index("ix_geopolitical_events_risk_level", "risk_level"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[int | None] = mapped_column(ForeignKey("news_articles.id"), nullable=True)
    event_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    headline: Mapped[str] = mapped_column(String(300), index=True)
    description: Mapped[str] = mapped_column(Text)
    oil_impact: Mapped[OilImpact] = mapped_column(Enum(OilImpact), default=OilImpact.NEUTRAL)
    sentiment: Mapped[float] = mapped_column(Float, default=0.0)
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), default=RiskLevel.MEDIUM)
    categories: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    affected_assets: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    affected_regions: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.5)
    source: Mapped[str] = mapped_column(String(120))
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)

    article: Mapped[NewsArticle | None] = relationship(back_populates="events")
