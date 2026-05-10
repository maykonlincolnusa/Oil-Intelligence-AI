from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.schemas.maritime import ChokepointOut, MaritimeRiskSummaryResponse, TankerRouteOut, VesselOut
from app.services.maritime_service import MaritimeService

router = APIRouter(prefix="/api/maritime", tags=["maritime"])


@router.get("/chokepoints", response_model=list[ChokepointOut])
async def get_chokepoints(session: AsyncSession = Depends(get_session)) -> list[ChokepointOut]:
    service = MaritimeService(session)
    items = await service.list_chokepoints()
    return [ChokepointOut(**row) for row in items]


@router.get("/vessels", response_model=list[VesselOut])
async def get_vessels(
    limit: int = Query(default=100, ge=1, le=1000),
    session: AsyncSession = Depends(get_session),
) -> list[VesselOut]:
    service = MaritimeService(session)
    items = await service.list_vessels(limit=limit)
    return [VesselOut(**row) for row in items]


@router.get("/risk-summary", response_model=MaritimeRiskSummaryResponse)
async def get_risk_summary(session: AsyncSession = Depends(get_session)) -> MaritimeRiskSummaryResponse:
    service = MaritimeService(session)
    data = await service.risk_summary()
    return MaritimeRiskSummaryResponse(**data)


@router.get("/routes", response_model=list[TankerRouteOut])
async def get_routes(
    limit: int = Query(default=100, ge=1, le=1000),
    session: AsyncSession = Depends(get_session),
) -> list[TankerRouteOut]:
    service = MaritimeService(session)
    items = await service.list_routes(limit=limit)
    return [TankerRouteOut(**row) for row in items]
