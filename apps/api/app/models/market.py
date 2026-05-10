from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Enum, Index, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin
from app.models.enums import BenchmarkSymbol, FundamentalIndicator


class PriceSeries(Base, TimestampMixin):
    __tablename__ = "price_series"
    __table_args__ = (Index("ix_price_series_symbol_timestamp", "symbol", "timestamp"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[BenchmarkSymbol] = mapped_column(Enum(BenchmarkSymbol), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    open: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    high: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    low: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    close: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    value: Mapped[Decimal] = mapped_column(Numeric(12, 4))
    source: Mapped[str] = mapped_column(String(120))
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class FundamentalRecord(Base, TimestampMixin):
    __tablename__ = "fundamental_records"
    __table_args__ = (
        Index(
            "ix_fundamental_records_indicator_country_period",
            "indicator",
            "country",
            "period",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    indicator: Mapped[FundamentalIndicator] = mapped_column(Enum(FundamentalIndicator), index=True)
    country: Mapped[str] = mapped_column(String(80), default="Global", index=True)
    region: Mapped[str] = mapped_column(String(80), default="Global", index=True)
    product_type: Mapped[str] = mapped_column(String(80), default="crude")
    unit: Mapped[str] = mapped_column(String(50), default="mbbl")
    period: Mapped[date] = mapped_column(Date, index=True)
    value: Mapped[Decimal] = mapped_column(Numeric(14, 4))
    source: Mapped[str] = mapped_column(String(120))
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)
