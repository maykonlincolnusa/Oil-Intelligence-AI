from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.api.pagination import build_pagination_meta
from app.core.config import get_settings
from app.schemas.maritime import ChokepointOut, MaritimeRiskSummaryResponse, TankerRouteOut, VesselOut
from app.schemas.pagination import PaginatedResponse
from app.services.maritime_service import MaritimeService

router = APIRouter(prefix="/maritime", tags=["maritime-v1"])
settings = get_settings()


@router.get("/chokepoints", response_model=PaginatedResponse[ChokepointOut])
async def get_chokepoints(
    limit: int = Query(default=settings.default_page_limit, ge=1, le=settings.max_page_limit),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
) -> PaginatedResponse[ChokepointOut]:
    service = MaritimeService(session)
    rows = await service.list_chokepoints(limit=limit, offset=offset)
    total = await service.count_chokepoints()
    items = [ChokepointOut(**row) for row in rows]
    return PaginatedResponse[ChokepointOut](
        items=items,
        pagination=build_pagination_meta(
            total=total,
            limit=limit,
            offset=offset,
            returned_count=len(items),
        ),
    )


@router.get("/vessels", response_model=PaginatedResponse[VesselOut])
async def get_vessels(
    limit: int = Query(default=settings.default_page_limit, ge=1, le=settings.max_page_limit),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
) -> PaginatedResponse[VesselOut]:
    service = MaritimeService(session)
    rows = await service.list_vessels(limit=limit, offset=offset)
    total = await service.count_vessels()
    items = [VesselOut(**row) for row in rows]
    return PaginatedResponse[VesselOut](
        items=items,
        pagination=build_pagination_meta(
            total=total,
            limit=limit,
            offset=offset,
            returned_count=len(items),
        ),
    )


@router.get("/risk-summary", response_model=MaritimeRiskSummaryResponse)
async def get_risk_summary(session: AsyncSession = Depends(get_session)) -> MaritimeRiskSummaryResponse:
    service = MaritimeService(session)
    data = await service.risk_summary()
    return MaritimeRiskSummaryResponse(**data)


@router.get("/routes", response_model=PaginatedResponse[TankerRouteOut])
async def get_routes(
    limit: int = Query(default=settings.default_page_limit, ge=1, le=settings.max_page_limit),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
) -> PaginatedResponse[TankerRouteOut]:
    service = MaritimeService(session)
    rows = await service.list_routes(limit=limit, offset=offset)
    total = await service.count_routes()
    items = [TankerRouteOut(**row) for row in rows]
    return PaginatedResponse[TankerRouteOut](
        items=items,
        pagination=build_pagination_meta(
            total=total,
            limit=limit,
            offset=offset,
            returned_count=len(items),
        ),
    )
