from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.schemas.alert import AlertEvaluationResponse, AlertEventOut, AlertRuleOut
from app.services.alert_service import AlertService

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("/rules", response_model=list[AlertRuleOut])
async def get_alert_rules(session: AsyncSession = Depends(get_session)) -> list[AlertRuleOut]:
    service = AlertService(session)
    rules = await service.list_rules()
    return [
        AlertRuleOut(
            rule_key=rule.rule_key,
            name=rule.name,
            description=rule.description,
            threshold=rule.threshold,
            comparator=rule.comparator,
            enabled=rule.enabled,
        )
        for rule in rules
    ]


@router.get("/events", response_model=list[AlertEventOut])
async def get_alert_events(
    limit: int = Query(default=50, ge=1, le=500),
    session: AsyncSession = Depends(get_session),
) -> list[AlertEventOut]:
    service = AlertService(session)
    events = await service.list_events(limit=limit)
    return [
        AlertEventOut(
            rule_key=event.rule_key,
            triggered_at=event.triggered_at,
            severity=event.severity,
            message=event.message,
            metric_value=event.metric_value,
            threshold_value=event.threshold_value,
            is_active=event.is_active,
        )
        for event in events
    ]


@router.post("/evaluate", response_model=AlertEvaluationResponse)
async def evaluate_alerts(session: AsyncSession = Depends(get_session)) -> AlertEvaluationResponse:
    service = AlertService(session)
    payload = await service.evaluate()
    return AlertEvaluationResponse(**payload)
