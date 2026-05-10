from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field


class PricePoint(BaseModel):
    symbol: str
    timestamp: datetime
    open: float | None = None
    high: float | None = None
    low: float | None = None
    close: float | None = None
    value: float
    source: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class PriceResponse(BaseModel):
    items: list[PricePoint]


class FundamentalPoint(BaseModel):
    indicator: str
    country: str
    region: str
    product_type: str
    unit: str
    period: date
    value: float
    source: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class FundamentalsResponse(BaseModel):
    items: list[FundamentalPoint]
