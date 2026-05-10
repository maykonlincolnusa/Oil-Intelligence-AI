from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    environment: str


class DependencyHealth(BaseModel):
    name: str
    status: Literal["ok", "error"]
    latency_ms: float | None = None
    detail: str | None = None


class ReadinessResponse(BaseModel):
    status: Literal["ok", "degraded"]
    service: str
    environment: str
    checked_at: datetime
    dependencies: list[DependencyHealth]
