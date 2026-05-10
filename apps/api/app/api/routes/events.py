from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.schemas.event import EventClassifyRequest, EventClassifyResponse, EventOut, EventsResponse
from app.services.event_service import EventService

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("", response_model=EventsResponse)
async def get_events(
    limit: int = Query(default=100, ge=1, le=500),
    session: AsyncSession = Depends(get_session),
) -> EventsResponse:
    service = EventService(session)
    rows = await service.get_events(limit=limit)
    return EventsResponse(
        items=[
            EventOut(
                id=row.id,
                event_time=row.event_time,
                headline=row.headline,
                description=row.description,
                oil_impact=row.oil_impact,
                sentiment=row.sentiment,
                risk_level=row.risk_level,
                categories=row.categories,
                affected_assets=row.affected_assets,
                affected_regions=row.affected_regions,
                confidence_score=row.confidence_score,
                source=row.source,
                metadata=row.metadata_json,
            )
            for row in rows
        ]
    )


@router.post("/classify", response_model=EventClassifyResponse)
async def classify_event(
    payload: EventClassifyRequest,
    session: AsyncSession = Depends(get_session),
) -> EventClassifyResponse:
    service = EventService(session)
    result = await service.classify_event(headline=payload.headline, description=payload.description)
    return EventClassifyResponse(**result)
