from sqlalchemy import Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin
from app.models.enums import Severity


class Scenario(Base, TimestampMixin):
    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    event_description: Mapped[str] = mapped_column(Text)
    affected_region: Mapped[str] = mapped_column(String(100))
    affected_asset: Mapped[str] = mapped_column(String(150))
    horizon_days: Mapped[int] = mapped_column(Integer)
    severity: Mapped[Severity] = mapped_column(Enum(Severity))

    executive_summary: Mapped[str] = mapped_column(Text)
    base_case: Mapped[str] = mapped_column(Text)
    bullish_case: Mapped[str] = mapped_column(Text)
    bearish_case: Mapped[str] = mapped_column(Text)
    operational_impact: Mapped[str] = mapped_column(Text)
    affected_sectors: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    confidence: Mapped[float] = mapped_column(default=0.6)
    recommended_monitoring_signals: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)
