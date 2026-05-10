from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import WellStatus
from app.models.field import OilField, Well, WellProduction


class FieldRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_fields(self) -> list[OilField]:
        result = await self.session.execute(select(OilField).order_by(OilField.name))
        return list(result.scalars().all())

    async def active_well_count(self, field_id: int) -> int:
        result = await self.session.execute(
            select(func.count(Well.id)).where(
                Well.field_id == field_id,
                Well.status == WellStatus.ACTIVE,
            )
        )
        return int(result.scalar() or 0)

    async def latest_production_total(self, field_id: int) -> float:
        result = await self.session.execute(
            select(func.sum(WellProduction.oil_bpd))
            .join(Well, Well.id == WellProduction.well_id)
            .where(Well.field_id == field_id)
        )
        return float(result.scalar() or 0.0)

    async def production_samples(self, limit: int = 20) -> list[tuple[str, WellProduction]]:
        result = await self.session.execute(
            select(Well.name, WellProduction)
            .join(Well, Well.id == WellProduction.well_id)
            .order_by(WellProduction.period_date.desc())
            .limit(limit)
        )
        return [(row[0], row[1]) for row in result.all()]
