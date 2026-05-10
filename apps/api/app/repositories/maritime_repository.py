from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.maritime import Chokepoint, MaritimeAnomaly, TankerRoute, Vessel


class MaritimeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_chokepoints(self, limit: int = 500, offset: int = 0) -> list[Chokepoint]:
        result = await self.session.execute(
            select(Chokepoint).order_by(Chokepoint.name).offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    async def count_chokepoints(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(Chokepoint))
        return int(result.scalar_one())

    async def get_vessels(self, limit: int = 100, offset: int = 0) -> list[Vessel]:
        result = await self.session.execute(
            select(Vessel).order_by(Vessel.name).offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    async def count_vessels(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(Vessel))
        return int(result.scalar_one())

    async def get_anomalies(self) -> list[MaritimeAnomaly]:
        result = await self.session.execute(
            select(MaritimeAnomaly).order_by(desc(MaritimeAnomaly.detected_at)).limit(50)
        )
        return list(result.scalars().all())

    async def get_high_risk_routes(self, threshold: int = 70) -> list[TankerRoute]:
        result = await self.session.execute(
            select(TankerRoute).where(TankerRoute.route_risk_score >= threshold)
        )
        return list(result.scalars().all())

    async def get_routes(self, limit: int = 100, offset: int = 0) -> list[dict]:
        result = await self.session.execute(
            select(TankerRoute)
            .order_by(desc(TankerRoute.route_risk_score))
            .offset(offset)
            .limit(limit)
        )
        rows = list(result.scalars().all())
        payload: list[dict] = []
        for route in rows:
            geojson = route.route_geojson if hasattr(route, "route_geojson") else {}
            coordinates = geojson.get("coordinates", []) if isinstance(geojson, dict) else []
            payload.append(
                {
                    "route_id": route.id,
                    "route_risk_score": route.route_risk_score,
                    "status": route.status,
                    "coordinates": coordinates,
                    "vessel_name": str(route.vessel_id),
                    "origin_port": None,
                    "destination_port": None,
                }
            )
        return payload

    async def count_routes(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(TankerRoute))
        return int(result.scalar_one())
