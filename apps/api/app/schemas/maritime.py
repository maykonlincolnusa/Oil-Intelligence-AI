from datetime import datetime

from pydantic import BaseModel


class ChokepointOut(BaseModel):
    name: str
    region: str
    description: str
    latitude: float
    longitude: float
    risk_level: str


class VesselOut(BaseModel):
    id: int
    imo: str
    name: str
    vessel_type: str
    flag: str
    deadweight_tons: int | None = None
    last_known_latitude: float | None = None
    last_known_longitude: float | None = None


class TankerRouteOut(BaseModel):
    route_id: int
    vessel_name: str
    origin_port: str | None = None
    destination_port: str | None = None
    route_risk_score: int
    status: str
    coordinates: list[list[float]]


class MaritimeRiskSummaryResponse(BaseModel):
    maritime_risk_score: int
    active_anomalies: int
    high_risk_routes: int
    chokepoint_alerts: list[str]
    generated_at: datetime
