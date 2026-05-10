from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import SatelliteRepository


class SatelliteService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = SatelliteRepository(session)

    async def summary(self) -> dict:
        observations = await self.repo.recent_observations(limit=100)
        fires = await self.repo.fire_events(limit=100)
        spills = await self.repo.spill_events(limit=100)
        storage_sites = await self.repo.storage_sites()
        refinery_sites = await self.repo.refinery_sites()

        alerts: list[str] = []
        if fires:
            alerts.append(f"{len(fires)} active thermal anomalies near monitored energy assets")
        if spills:
            alerts.append(f"{len(spills)} potential spill signatures flagged for analyst review")
        if not alerts:
            alerts.append("No high-priority remote sensing alerts in current mock feed")

        return {
            "recent_observations": len(observations),
            "active_fire_events": len(fires),
            "potential_oil_spills": len(spills),
            "monitored_storage_sites": len(storage_sites),
            "monitored_refineries": len(refinery_sites),
            "top_alerts": alerts,
        }
