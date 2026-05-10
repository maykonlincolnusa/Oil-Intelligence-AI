from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin
from app.models.enums import VesselType


class Vessel(Base, TimestampMixin):
    __tablename__ = "vessels"

    id: Mapped[int] = mapped_column(primary_key=True)
    imo: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160), index=True)
    vessel_type: Mapped[VesselType] = mapped_column(Enum(VesselType), index=True)
    flag: Mapped[str] = mapped_column(String(80), default="Unknown")
    deadweight_tons: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # PostGIS-ready placeholders. Replace with Geometry(Point, 4326) when extension is active.
    last_known_latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    last_known_longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    location_wkt: Mapped[str | None] = mapped_column(String(180), nullable=True)
    location_geojson: Mapped[dict] = mapped_column(JSONB, default=dict)
    location_srid: Mapped[int] = mapped_column(Integer, default=4326)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class VesselPosition(Base, TimestampMixin):
    __tablename__ = "vessel_positions"
    __table_args__ = (Index("ix_vessel_positions_vessel_timestamp", "vessel_id", "timestamp"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    vessel_id: Mapped[int] = mapped_column(ForeignKey("vessels.id"), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    position_wkt: Mapped[str | None] = mapped_column(String(180), nullable=True)
    speed_knots: Mapped[float | None] = mapped_column(Float, nullable=True)
    course_degrees: Mapped[float | None] = mapped_column(Float, nullable=True)
    nav_status: Mapped[str | None] = mapped_column(String(80), nullable=True)


class Port(Base, TimestampMixin):
    __tablename__ = "ports"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), index=True)
    country: Mapped[str] = mapped_column(String(80), index=True)
    region: Mapped[str] = mapped_column(String(80), index=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    location_wkt: Mapped[str | None] = mapped_column(String(180), nullable=True)
    location_geojson: Mapped[dict] = mapped_column(JSONB, default=dict)
    location_srid: Mapped[int] = mapped_column(Integer, default=4326)
    is_oil_terminal: Mapped[bool] = mapped_column(Boolean, default=False)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class Chokepoint(Base, TimestampMixin):
    __tablename__ = "chokepoints"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    region: Mapped[str] = mapped_column(String(120), index=True)
    description: Mapped[str] = mapped_column(Text)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    location_wkt: Mapped[str | None] = mapped_column(String(180), nullable=True)
    location_geojson: Mapped[dict] = mapped_column(JSONB, default=dict)
    location_srid: Mapped[int] = mapped_column(Integer, default=4326)
    risk_level: Mapped[str] = mapped_column(String(30), default="medium")
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class TankerRoute(Base, TimestampMixin):
    __tablename__ = "tanker_routes"

    id: Mapped[int] = mapped_column(primary_key=True)
    vessel_id: Mapped[int] = mapped_column(ForeignKey("vessels.id"), index=True)
    origin_port_id: Mapped[int | None] = mapped_column(ForeignKey("ports.id"), nullable=True)
    destination_port_id: Mapped[int | None] = mapped_column(ForeignKey("ports.id"), nullable=True)
    eta: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="in_transit")
    route_risk_score: Mapped[int] = mapped_column(Integer, default=40)
    route_wkt: Mapped[str | None] = mapped_column(Text, nullable=True)
    route_geojson: Mapped[dict] = mapped_column(JSONB, default=dict)
    route_srid: Mapped[int] = mapped_column(Integer, default=4326)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class PortCall(Base, TimestampMixin):
    __tablename__ = "port_calls"

    id: Mapped[int] = mapped_column(primary_key=True)
    vessel_id: Mapped[int] = mapped_column(ForeignKey("vessels.id"), index=True)
    port_id: Mapped[int] = mapped_column(ForeignKey("ports.id"), index=True)
    arrival_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    departure_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cargo_type: Mapped[str] = mapped_column(String(100), default="crude")
    status: Mapped[str] = mapped_column(String(50), default="scheduled")


class MaritimeAnomaly(Base, TimestampMixin):
    __tablename__ = "maritime_anomalies"

    id: Mapped[int] = mapped_column(primary_key=True)
    vessel_id: Mapped[int | None] = mapped_column(ForeignKey("vessels.id"), nullable=True)
    chokepoint_id: Mapped[int | None] = mapped_column(ForeignKey("chokepoints.id"), nullable=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    anomaly_type: Mapped[str] = mapped_column(String(120), index=True)
    severity: Mapped[str] = mapped_column(String(30), default="medium")
    description: Mapped[str] = mapped_column(Text)
    risk_score: Mapped[int] = mapped_column(Integer, default=50)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)
