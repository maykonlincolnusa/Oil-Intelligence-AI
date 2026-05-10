from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin
from app.models.enums import WellStatus, WellType


class OilField(Base, TimestampMixin):
    __tablename__ = "oil_fields"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), index=True)
    country: Mapped[str] = mapped_column(String(80), index=True)
    basin: Mapped[str] = mapped_column(String(120))
    operator: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(50), default="producing")
    start_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class Reservoir(Base, TimestampMixin):
    __tablename__ = "reservoirs"

    id: Mapped[int] = mapped_column(primary_key=True)
    field_id: Mapped[int] = mapped_column(ForeignKey("oil_fields.id"), index=True)
    name: Mapped[str] = mapped_column(String(150))
    formation: Mapped[str] = mapped_column(String(120))
    drive_mechanism: Mapped[str] = mapped_column(String(120), default="water_drive")
    estimated_ooip_mmbbl: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(50), default="active")
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class Well(Base, TimestampMixin):
    __tablename__ = "wells"

    id: Mapped[int] = mapped_column(primary_key=True)
    field_id: Mapped[int] = mapped_column(ForeignKey("oil_fields.id"), index=True)
    reservoir_id: Mapped[int | None] = mapped_column(ForeignKey("reservoirs.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(150), index=True)
    well_type: Mapped[WellType] = mapped_column(Enum(WellType), default=WellType.PRODUCER)
    status: Mapped[WellStatus] = mapped_column(Enum(WellStatus), default=WellStatus.ACTIVE)
    spud_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class WellProduction(Base, TimestampMixin):
    __tablename__ = "well_production"

    id: Mapped[int] = mapped_column(primary_key=True)
    well_id: Mapped[int] = mapped_column(ForeignKey("wells.id"), index=True)
    period_date: Mapped[date] = mapped_column(Date, index=True)
    oil_bpd: Mapped[float] = mapped_column(Float)
    gas_mmscfd: Mapped[float | None] = mapped_column(Float, nullable=True)
    water_bpd: Mapped[float | None] = mapped_column(Float, nullable=True)
    source: Mapped[str] = mapped_column(String(120), default="Volve Mock Loader")
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class ProductionForecast(Base, TimestampMixin):
    __tablename__ = "production_forecasts"

    id: Mapped[int] = mapped_column(primary_key=True)
    field_id: Mapped[int] = mapped_column(ForeignKey("oil_fields.id"), index=True)
    horizon_days: Mapped[int] = mapped_column(Integer)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    base_case_bpd: Mapped[float] = mapped_column(Float)
    bullish_case_bpd: Mapped[float] = mapped_column(Float)
    bearish_case_bpd: Mapped[float] = mapped_column(Float)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.65)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class DeclineCurveAnalysis(Base, TimestampMixin):
    __tablename__ = "decline_curve_analyses"

    id: Mapped[int] = mapped_column(primary_key=True)
    well_id: Mapped[int] = mapped_column(ForeignKey("wells.id"), index=True)
    model_type: Mapped[str] = mapped_column(String(80), default="hyperbolic")
    qi: Mapped[float] = mapped_column(Float)
    di: Mapped[float] = mapped_column(Float)
    b_factor: Mapped[float] = mapped_column(Float)
    forecast_horizon_days: Mapped[int] = mapped_column(Integer)
    r_squared: Mapped[float] = mapped_column(Float)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)
