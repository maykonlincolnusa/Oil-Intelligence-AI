from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.api.pagination import build_pagination_meta
from app.core.config import get_settings
from app.schemas.event import EventClassifyRequest, EventClassifyResponse, EventOut
from app.schemas.pagination import PaginatedResponse
from app.services.event_service import EventService

router = APIRouter(prefix="/events", tags=["events-v1"])
settings = get_settings()


@router.get("", response_model=PaginatedResponse[EventOut])
async def get_events(
    limit: int = Query(default=settings.default_page_limit, ge=1, le=settings.max_page_limit),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
) -> PaginatedResponse[EventOut]:
    service = EventService(session)
    rows = await service.get_events(limit=limit, offset=offset)
    total = await service.count_events()

    items = [
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

    return PaginatedResponse[EventOut](
        items=items,
        pagination=build_pagination_meta(
            total=total,
            limit=limit,
            offset=offset,
            returned_count=len(items),
        ),
    )


@router.post("/classify", response_model=EventClassifyResponse)
async def classify_event(
    payload: EventClassifyRequest,
    session: AsyncSession = Depends(get_session),
) -> EventClassifyResponse:
    service = EventService(session)
    result = await service.classify_event(headline=payload.headline, description=payload.description)
    return EventClassifyResponse(**result)
