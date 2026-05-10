from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.schemas.scenario import ScenarioGenerateRequest, ScenarioGenerateResponse
from app.services.scenario_service import ScenarioService

router = APIRouter(prefix="/scenarios", tags=["scenarios-v1"])


@router.post("/generate", response_model=ScenarioGenerateResponse)
async def generate_scenario(
    payload: ScenarioGenerateRequest,
    session: AsyncSession = Depends(get_session),
) -> ScenarioGenerateResponse:
    service = ScenarioService(session)
    data = await service.generate(
        title=payload.scenario_title,
        event_description=payload.event_description,
        affected_region=payload.affected_region,
        affected_asset=payload.affected_asset,
        horizon_days=payload.horizon_days,
        severity=payload.severity,
    )
    return ScenarioGenerateResponse(**data)
