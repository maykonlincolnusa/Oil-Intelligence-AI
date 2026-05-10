from datetime import date, datetime

from pydantic import BaseModel, Field


class DailyReportMover(BaseModel):
    symbol: str
    last_price: float
    change_percent: float


class DailyReportEvent(BaseModel):
    headline: str
    risk_level: str
    oil_impact: str
    confidence_score: float


class DailyReportResponse(BaseModel):
    report_date: date
    market_summary: str
    brent_wti_summary: str
    top_price_movers: list[DailyReportMover]
    top_geopolitical_events: list[DailyReportEvent]
    top_risk_drivers: list[str]
    fundamentals_summary: str
    risk_score: int
    maritime_risk_score: int
    refinery_storage_alerts: list[str]
    scenario_watchlist: list[str]
    ai_analyst_conclusion: str
    disclaimer: str
    executive_summary: str
    confidence: float
    generated_at: datetime


class DailyReportPDFResponse(BaseModel):
    filename: str = Field(default="oil-intelligence-daily-report.pdf")
