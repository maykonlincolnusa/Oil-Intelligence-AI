from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.satellite import FireEvent, OilSpillObservation, RefinerySite, SatelliteObservation, StorageSite


class SatelliteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def recent_observations(self, limit: int = 50) -> list[SatelliteObservation]:
        result = await self.session.execute(
            select(SatelliteObservation).order_by(desc(SatelliteObservation.observed_at)).limit(limit)
        )
        return list(result.scalars().all())

    async def fire_events(self, limit: int = 50) -> list[FireEvent]:
        result = await self.session.execute(select(FireEvent).order_by(desc(FireEvent.detected_at)).limit(limit))
        return list(result.scalars().all())

    async def spill_events(self, limit: int = 50) -> list[OilSpillObservation]:
        result = await self.session.execute(
            select(OilSpillObservation).order_by(desc(OilSpillObservation.observed_at)).limit(limit)
        )
        return list(result.scalars().all())

    async def storage_sites(self) -> list[StorageSite]:
        result = await self.session.execute(select(StorageSite))
        return list(result.scalars().all())

    async def refinery_sites(self) -> list[RefinerySite]:
        result = await self.session.execute(select(RefinerySite))
        return list(result.scalars().all())
