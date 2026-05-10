from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.schemas.risk import RiskSummaryResponse
from app.services.risk_scoring_service import RiskScoringService

router = APIRouter(prefix="/risk", tags=["risk-v1"])


@router.get("/summary", response_model=RiskSummaryResponse)
async def get_risk_summary(session: AsyncSession = Depends(get_session)) -> RiskSummaryResponse:
    service = RiskScoringService(session)
    data = await service.calculate()
    return RiskSummaryResponse(**data)
