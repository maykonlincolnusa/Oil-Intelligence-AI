from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.clients import EIAClient, FREDClient
from app.core.config import get_settings
from app.models.market import FundamentalRecord, PriceSeries
from app.repositories import FundamentalsRepository, MarketRepository


class MarketDataService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        settings = get_settings()
        self.market_repo = MarketRepository(session)
        self.fundamentals_repo = FundamentalsRepository(session)
        self.eia_client = EIAClient(api_key=settings.eia_api_key)
        self.fred_client = FREDClient(api_key=settings.fred_api_key)

    async def get_prices(
        self,
        symbol: str | None = None,
        limit: int = 120,
        offset: int = 0,
    ) -> list[PriceSeries]:
        rows = await self.market_repo.get_prices(symbol=symbol, limit=limit, offset=offset)
        if rows:
            return rows
        await self.bootstrap_market_data()
        return await self.market_repo.get_prices(symbol=symbol, limit=limit, offset=offset)

    async def count_prices(self, symbol: str | None = None) -> int:
        return await self.market_repo.count_prices(symbol=symbol)

    async def get_fundamentals(
        self,
        indicator: str | None = None,
        country: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        limit: int = 200,
        offset: int = 0,
    ) -> list[FundamentalRecord]:
        rows = await self.fundamentals_repo.get_fundamentals(
            indicator=indicator,
            country=country,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset,
        )
        if rows:
            return rows
        await self.bootstrap_fundamentals()
        return await self.fundamentals_repo.get_fundamentals(
            indicator=indicator,
            country=country,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset,
        )

    async def count_fundamentals(
        self,
        indicator: str | None = None,
        country: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> int:
        return await self.fundamentals_repo.count_fundamentals(
            indicator=indicator,
            country=country,
            start_date=start_date,
            end_date=end_date,
        )

    async def bootstrap_market_data(self) -> None:
        for symbol in ["BRENT", "WTI"]:
            points = await self.eia_client.get_crude_prices(symbol=symbol, days=45)
            for p in points:
                self.session.add(
                    PriceSeries(
                        symbol=p["symbol"],
                        timestamp=p["timestamp"],
                        open=p["open"],
                        high=p["high"],
                        low=p["low"],
                        close=p["close"],
                        value=p["value"],
                        source=p["source"],
                        metadata_json=p["metadata"],
                    )
                )
        await self.session.commit()

    async def bootstrap_fundamentals(self) -> None:
        rows = await self.fred_client.get_fundamentals(days=30)
        for row in rows:
            self.session.add(
                FundamentalRecord(
                    indicator=row["indicator"],
                    country=row["country"],
                    region=row["region"],
                    product_type=row["product_type"],
                    unit=row["unit"],
                    period=row["period"],
                    value=row["value"],
                    source=row["source"],
                    metadata_json=row["metadata"],
                )
            )
        await self.session.commit()
