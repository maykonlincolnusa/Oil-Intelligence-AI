from typing import Any

from pydantic import BaseModel, Field


class RiskSummaryResponse(BaseModel):
    global_risk_score: int
    geopolitical_risk_score: int
    maritime_risk_score: int
    supply_risk_score: int
    demand_risk_score: int
    refinery_risk_score: int
    volatility_score: int
    level: str
    drivers: list[str] = Field(default_factory=list)
    recent_events: list[str] = Field(default_factory=list)
    affected_regions: list[str] = Field(default_factory=list)
    affected_assets: list[str] = Field(default_factory=list)
    confidence: float
    details: dict[str, Any] = Field(default_factory=dict)
