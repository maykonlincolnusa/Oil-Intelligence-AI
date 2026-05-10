from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class RiskSnapshot(Base, TimestampMixin):
    __tablename__ = "risk_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True)
    global_risk_score: Mapped[int] = mapped_column(Integer)
    geopolitical_risk_score: Mapped[int] = mapped_column(Integer)
    maritime_risk_score: Mapped[int] = mapped_column(Integer)
    supply_risk_score: Mapped[int] = mapped_column(Integer)
    demand_risk_score: Mapped[int] = mapped_column(Integer)
    refinery_risk_score: Mapped[int] = mapped_column(Integer)
    details: Mapped[dict] = mapped_column(JSONB, default=dict)


class AlertRule(Base, TimestampMixin):
    __tablename__ = "alert_rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    rule_key: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(180))
    description: Mapped[str] = mapped_column(Text)
    threshold: Mapped[float] = mapped_column(Float)
    comparator: Mapped[str] = mapped_column(String(10), default=">")
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class AlertEvent(Base, TimestampMixin):
    __tablename__ = "alert_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    rule_key: Mapped[str] = mapped_column(String(80), index=True)
    triggered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    severity: Mapped[str] = mapped_column(String(20), default="medium")
    message: Mapped[str] = mapped_column(Text)
    metric_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    threshold_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class DailyIntelligenceReport(Base, TimestampMixin):
    __tablename__ = "daily_intelligence_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    report_date: Mapped[date] = mapped_column(Date, index=True, unique=True)
    market_summary: Mapped[str] = mapped_column(Text)
    top_price_movers: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    top_geopolitical_events: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    risk_score: Mapped[int] = mapped_column(Integer)
    maritime_risk_score: Mapped[int] = mapped_column(Integer)
    refinery_storage_alerts: Mapped[list[str]] = mapped_column(JSONB, default=list)
    scenario_watchlist: Mapped[list[str]] = mapped_column(JSONB, default=list)
    executive_summary: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float, default=0.65)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)
