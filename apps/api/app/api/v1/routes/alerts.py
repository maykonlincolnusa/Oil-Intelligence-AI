from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.api.pagination import build_pagination_meta
from app.core.config import get_settings
from app.schemas.alert import AlertEvaluationResponse, AlertEventOut, AlertRuleOut
from app.schemas.pagination import PaginatedResponse
from app.services.alert_service import AlertService

router = APIRouter(prefix="/alerts", tags=["alerts-v1"])
settings = get_settings()


@router.get("/rules", response_model=PaginatedResponse[AlertRuleOut])
async def get_alert_rules(
    limit: int = Query(default=settings.default_page_limit, ge=1, le=settings.max_page_limit),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
) -> PaginatedResponse[AlertRuleOut]:
    service = AlertService(session)
    rules = await service.list_rules(limit=limit, offset=offset)
    total = await service.count_rules()
    items = [
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
    return PaginatedResponse[AlertRuleOut](
        items=items,
        pagination=build_pagination_meta(
            total=total,
            limit=limit,
            offset=offset,
            returned_count=len(items),
        ),
    )


@router.get("/events", response_model=PaginatedResponse[AlertEventOut])
async def get_alert_events(
    limit: int = Query(default=settings.default_page_limit, ge=1, le=settings.max_page_limit),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
) -> PaginatedResponse[AlertEventOut]:
    service = AlertService(session)
    events = await service.list_events(limit=limit, offset=offset)
    total = await service.count_events()
    items = [
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
    return PaginatedResponse[AlertEventOut](
        items=items,
        pagination=build_pagination_meta(
            total=total,
            limit=limit,
            offset=offset,
            returned_count=len(items),
        ),
    )


@router.post("/evaluate", response_model=AlertEvaluationResponse)
async def evaluate_alerts(session: AsyncSession = Depends(get_session)) -> AlertEvaluationResponse:
    service = AlertService(session)
    payload = await service.evaluate()
    return AlertEvaluationResponse(**payload)
