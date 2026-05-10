from datetime import datetime, timedelta, timezone

from sqlalchemy import Select, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import GeopoliticalEvent
from app.repositories.base import BaseRepository


class EventRepository(BaseRepository[GeopoliticalEvent]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, GeopoliticalEvent)

    async def get_events(self, limit: int = 100, offset: int = 0) -> list[GeopoliticalEvent]:
        result = await self.session.execute(
            select(GeopoliticalEvent)
            .order_by(desc(GeopoliticalEvent.event_time))
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def count_events(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(GeopoliticalEvent))
        return int(result.scalar_one())

    async def get_recent_events(self, days: int = 14) -> list[GeopoliticalEvent]:
        since = datetime.now(timezone.utc) - timedelta(days=days)
        query: Select[tuple[GeopoliticalEvent]] = select(GeopoliticalEvent).where(
            GeopoliticalEvent.event_time >= since
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())
