from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class EventOut(BaseModel):
    id: int
    event_time: datetime
    headline: str
    description: str
    oil_impact: str
    sentiment: float
    risk_level: str
    categories: list[str] = Field(default_factory=list)
    affected_assets: list[str] = Field(default_factory=list)
    affected_regions: list[str] = Field(default_factory=list)
    confidence_score: float
    source: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class EventsResponse(BaseModel):
    items: list[EventOut]


class EventClassifyRequest(BaseModel):
    headline: str
    description: str
    source: str = "manual"


class EventClassifyResponse(BaseModel):
    oil_impact: str
    sentiment: float
    risk_level: str
    categories: list[str]
    affected_assets: list[str]
    affected_regions: list[str]
    confidence_score: float
    reasoning: str
