from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.schemas.market import FundamentalPoint, FundamentalsResponse, PricePoint, PriceResponse
from app.services.market_data_service import MarketDataService

router = APIRouter(prefix="/api/market", tags=["market"])


@router.get("/prices", response_model=PriceResponse)
async def get_prices(
    symbol: str | None = Query(default=None),
    limit: int = Query(default=120, ge=1, le=1000),
    session: AsyncSession = Depends(get_session),
) -> PriceResponse:
    service = MarketDataService(session)
    rows = await service.get_prices(symbol=symbol, limit=limit)
    return PriceResponse(
        items=[
            PricePoint(
                symbol=row.symbol,
                timestamp=row.timestamp,
                open=float(row.open) if row.open is not None else None,
                high=float(row.high) if row.high is not None else None,
                low=float(row.low) if row.low is not None else None,
                close=float(row.close) if row.close is not None else None,
                value=float(row.value),
                source=row.source,
                metadata=row.metadata_json,
            )
            for row in rows
        ]
    )


@router.get("/fundamentals", response_model=FundamentalsResponse)
async def get_fundamentals(
    indicator: str | None = Query(default=None),
    country: str | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=2000),
    session: AsyncSession = Depends(get_session),
) -> FundamentalsResponse:
    service = MarketDataService(session)
    rows = await service.get_fundamentals(
        indicator=indicator,
        country=country,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    )
    return FundamentalsResponse(
        items=[
            FundamentalPoint(
                indicator=row.indicator,
                country=row.country,
                region=row.region,
                product_type=row.product_type,
                unit=row.unit,
                period=row.period,
                value=float(row.value),
                source=row.source,
                metadata=row.metadata_json,
            )
            for row in rows
        ]
    )
