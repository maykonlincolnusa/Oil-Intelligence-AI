from typing import Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class ScenarioGenerateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    scenario_title: str = Field(validation_alias=AliasChoices("scenario_title", "title"))
    event_description: str
    affected_region: str
    affected_asset: str
    horizon_days: int = Field(gt=0, le=730)
    severity: Literal["low", "medium", "high", "extreme"]


class ScenarioGenerateResponse(BaseModel):
    executive_summary: str
    base_case: str
    bullish_case: str
    bearish_case: str
    operational_impact: str
    affected_sectors: list[str]
    price_pressure: str
    risk_drivers: list[str]
    monitoring_signals: list[str]
    confidence: float
    disclaimer: str
    recommended_monitoring_signals: list[str] = Field(default_factory=list)
