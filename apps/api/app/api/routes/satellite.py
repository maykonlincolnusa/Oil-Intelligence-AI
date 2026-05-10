from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.schemas.satellite import SatelliteSummaryResponse
from app.services.satellite_service import SatelliteService

router = APIRouter(prefix="/api/satellite", tags=["satellite"])


@router.get("/summary", response_model=SatelliteSummaryResponse)
async def get_satellite_summary(
    session: AsyncSession = Depends(get_session),
) -> SatelliteSummaryResponse:
    service = SatelliteService(session)
    data = await service.summary()
    return SatelliteSummaryResponse(**data)
