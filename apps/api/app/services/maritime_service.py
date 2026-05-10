from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import MaritimeRepository


class MaritimeService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = MaritimeRepository(session)

    async def list_chokepoints(self, limit: int = 500, offset: int = 0) -> list[dict]:
        rows = await self.repo.get_chokepoints(limit=limit, offset=offset)
        return [
            {
                "name": r.name,
                "region": r.region,
                "description": r.description,
                "latitude": r.latitude,
                "longitude": r.longitude,
                "risk_level": r.risk_level,
            }
            for r in rows
        ]

    async def count_chokepoints(self) -> int:
        return await self.repo.count_chokepoints()

    async def list_vessels(self, limit: int = 100, offset: int = 0) -> list[dict]:
        rows = await self.repo.get_vessels(limit=limit, offset=offset)
        return [
            {
                "id": r.id,
                "imo": r.imo,
                "name": r.name,
                "vessel_type": r.vessel_type,
                "flag": r.flag,
                "deadweight_tons": r.deadweight_tons,
                "last_known_latitude": r.last_known_latitude,
                "last_known_longitude": r.last_known_longitude,
            }
            for r in rows
        ]

    async def count_vessels(self) -> int:
        return await self.repo.count_vessels()

    async def list_routes(self, limit: int = 100, offset: int = 0) -> list[dict]:
        routes = await self.repo.get_routes(limit=limit, offset=offset)
        vessels = await self.repo.get_vessels(limit=1000)
        vessel_map = {str(v.id): v.name for v in vessels}
        for route in routes:
            route["vessel_name"] = vessel_map.get(route["vessel_name"], route["vessel_name"])
        return routes

    async def count_routes(self) -> int:
        return await self.repo.count_routes()

    async def risk_summary(self) -> dict:
        anomalies = await self.repo.get_anomalies()
        high_routes = await self.repo.get_high_risk_routes()
        chokepoints = await self.repo.get_chokepoints(limit=500, offset=0)

        alerts = [
            f"{a.anomaly_type} near vessel_id={a.vessel_id or 'N/A'} (score {a.risk_score})"
            for a in anomalies[:4]
        ]
        score = min(100, 35 + len(anomalies) * 6 + len(high_routes) * 5)

        if not alerts:
            alerts.append("No critical maritime anomalies in the latest sample window.")
        if chokepoints:
            alerts.append(f"{len(chokepoints)} chokepoints monitored in active watchlist")

        return {
            "maritime_risk_score": score,
            "active_anomalies": len(anomalies),
            "high_risk_routes": len(high_routes),
            "chokepoint_alerts": alerts,
            "generated_at": datetime.now(timezone.utc),
        }
