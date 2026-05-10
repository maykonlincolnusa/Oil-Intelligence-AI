from datetime import date

from sqlalchemy import Select, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import FundamentalIndicator
from app.models.market import FundamentalRecord, PriceSeries
from app.repositories.base import BaseRepository


class MarketRepository(BaseRepository[PriceSeries]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, PriceSeries)

    async def get_prices(
        self,
        symbol: str | None = None,
        limit: int = 120,
        offset: int = 0,
    ) -> list[PriceSeries]:
        query: Select[tuple[PriceSeries]] = select(PriceSeries)
        if symbol:
            query = query.where(PriceSeries.symbol == symbol.upper())
        query = query.order_by(desc(PriceSeries.timestamp)).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def count_prices(self, symbol: str | None = None) -> int:
        query = select(func.count()).select_from(PriceSeries)
        if symbol:
            query = query.where(PriceSeries.symbol == symbol.upper())
        result = await self.session.execute(query)
        return int(result.scalar_one())


class FundamentalsRepository(BaseRepository[FundamentalRecord]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, FundamentalRecord)

    def _parse_indicator(
        self,
        indicator: str | FundamentalIndicator | None,
    ) -> FundamentalIndicator | None:
        if indicator is None:
            return None
        if isinstance(indicator, FundamentalIndicator):
            return indicator

        indicator_upper = indicator.upper()
        try:
            return FundamentalIndicator(indicator.lower())
        except ValueError:
            if indicator_upper in FundamentalIndicator.__members__:
                return FundamentalIndicator[indicator_upper]
        return None

    def _build_query(
        self,
        indicator: str | FundamentalIndicator | None = None,
        country: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> Select[tuple[FundamentalRecord]]:
        query: Select[tuple[FundamentalRecord]] = select(FundamentalRecord)

        parsed_indicator = self._parse_indicator(indicator)
        if parsed_indicator is not None:
            query = query.where(FundamentalRecord.indicator == parsed_indicator)

        if country:
            query = query.where(FundamentalRecord.country == country)
        if start_date:
            query = query.where(FundamentalRecord.period >= start_date)
        if end_date:
            query = query.where(FundamentalRecord.period <= end_date)

        return query

    async def get_fundamentals(
        self,
        indicator: str | FundamentalIndicator | None = None,
        country: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        limit: int = 200,
        offset: int = 0,
    ) -> list[FundamentalRecord]:
        query = self._build_query(
            indicator=indicator,
            country=country,
            start_date=start_date,
            end_date=end_date,
        ).order_by(desc(FundamentalRecord.period)).offset(offset).limit(limit)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def count_fundamentals(
        self,
        indicator: str | FundamentalIndicator | None = None,
        country: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> int:
        base_query = self._build_query(
            indicator=indicator,
            country=country,
            start_date=start_date,
            end_date=end_date,
        )
        count_query = select(func.count()).select_from(base_query.subquery())
        result = await self.session.execute(count_query)
        return int(result.scalar_one())
