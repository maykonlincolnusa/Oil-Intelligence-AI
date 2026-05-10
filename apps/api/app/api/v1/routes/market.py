from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.api.pagination import build_pagination_meta
from app.core.config import get_settings
from app.schemas.market import FundamentalPoint, PricePoint
from app.schemas.pagination import PaginatedResponse
from app.services.market_data_service import MarketDataService

router = APIRouter(prefix="/market", tags=["market-v1"])
settings = get_settings()


@router.get("/prices", response_model=PaginatedResponse[PricePoint])
async def get_prices(
    symbol: str | None = Query(default=None),
    limit: int = Query(default=settings.default_page_limit, ge=1, le=settings.max_page_limit),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
) -> PaginatedResponse[PricePoint]:
    service = MarketDataService(session)
    rows = await service.get_prices(symbol=symbol, limit=limit, offset=offset)
    total = await service.count_prices(symbol=symbol)

    items = [
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
    return PaginatedResponse[PricePoint](
        items=items,
        pagination=build_pagination_meta(
            total=total,
            limit=limit,
            offset=offset,
            returned_count=len(items),
        ),
    )


@router.get("/fundamentals", response_model=PaginatedResponse[FundamentalPoint])
async def get_fundamentals(
    indicator: str | None = Query(default=None),
    country: str | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    limit: int = Query(default=settings.default_page_limit, ge=1, le=settings.max_page_limit),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
) -> PaginatedResponse[FundamentalPoint]:
    service = MarketDataService(session)
    rows = await service.get_fundamentals(
        indicator=indicator,
        country=country,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset,
    )
    total = await service.count_fundamentals(
        indicator=indicator,
        country=country,
        start_date=start_date,
        end_date=end_date,
    )

    items = [
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
    return PaginatedResponse[FundamentalPoint](
        items=items,
        pagination=build_pagination_meta(
            total=total,
            limit=limit,
            offset=offset,
            returned_count=len(items),
        ),
    )
