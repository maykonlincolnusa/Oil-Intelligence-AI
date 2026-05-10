from datetime import datetime

from pydantic import BaseModel


class AlertRuleOut(BaseModel):
    rule_key: str
    name: str
    description: str
    threshold: float
    comparator: str
    enabled: bool


class AlertEventOut(BaseModel):
    rule_key: str
    triggered_at: datetime
    severity: str
    message: str
    metric_value: float | None = None
    threshold_value: float | None = None
    is_active: bool


class AlertEvaluationResponse(BaseModel):
    evaluated_at: datetime
    triggered_count: int
    events: list[AlertEventOut]
