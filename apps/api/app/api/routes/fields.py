from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.schemas.field import FieldsSummaryResponse
from app.services.field_service import FieldService

router = APIRouter(prefix="/api/fields", tags=["fields"])


@router.get("/summary", response_model=FieldsSummaryResponse)
async def get_fields_summary(session: AsyncSession = Depends(get_session)) -> FieldsSummaryResponse:
    service = FieldService(session)
    data = await service.summary()
    return FieldsSummaryResponse(**data)
