from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class SatelliteObservation(Base, TimestampMixin):
    __tablename__ = "satellite_observations"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider: Mapped[str] = mapped_column(String(120))
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    location_wkt: Mapped[str | None] = mapped_column(String(180), nullable=True)
    location_geojson: Mapped[dict] = mapped_column(JSONB, default=dict)
    location_srid: Mapped[int] = mapped_column(Integer, default=4326)
    observation_type: Mapped[str] = mapped_column(String(120))
    confidence_score: Mapped[float] = mapped_column(Float, default=0.6)
    summary: Mapped[str] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class StorageSite(Base, TimestampMixin):
    __tablename__ = "storage_sites"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), index=True)
    country: Mapped[str] = mapped_column(String(80), index=True)
    region: Mapped[str] = mapped_column(String(80), index=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    location_wkt: Mapped[str | None] = mapped_column(String(180), nullable=True)
    location_geojson: Mapped[dict] = mapped_column(JSONB, default=dict)
    location_srid: Mapped[int] = mapped_column(Integer, default=4326)
    capacity_bbl: Mapped[int] = mapped_column(Integer)
    operator: Mapped[str] = mapped_column(String(120))
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class RefinerySite(Base, TimestampMixin):
    __tablename__ = "refinery_sites"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), index=True)
    country: Mapped[str] = mapped_column(String(80), index=True)
    region: Mapped[str] = mapped_column(String(80), index=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    location_wkt: Mapped[str | None] = mapped_column(String(180), nullable=True)
    location_geojson: Mapped[dict] = mapped_column(JSONB, default=dict)
    location_srid: Mapped[int] = mapped_column(Integer, default=4326)
    capacity_bpd: Mapped[int] = mapped_column(Integer)
    operator: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(50), default="operational")
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class FireEvent(Base, TimestampMixin):
    __tablename__ = "fire_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_name: Mapped[str] = mapped_column(String(150), index=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    intensity: Mapped[float] = mapped_column(Float)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.7)
    source: Mapped[str] = mapped_column(String(80), default="NASA FIRMS")
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class OilSpillObservation(Base, TimestampMixin):
    __tablename__ = "oil_spill_observations"

    id: Mapped[int] = mapped_column(primary_key=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    estimated_area_km2: Mapped[float] = mapped_column(Float)
    severity: Mapped[str] = mapped_column(String(30), default="medium")
    source: Mapped[str] = mapped_column(String(120), default="Sentinel Hub")
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)