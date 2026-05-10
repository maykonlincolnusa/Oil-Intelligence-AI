import asyncio

from app.core.database import SessionLocal
from app.services.alert_service import AlertService
from app.services.event_service import EventService
from app.services.market_data_service import MarketDataService
from app.workers.celery_app import celery_app


@celery_app.task(name="app.workers.tasks.refresh_market_data")
def refresh_market_data() -> str:
    return asyncio.run(_refresh_market_data())


async def _refresh_market_data() -> str:
    async with SessionLocal() as session:
        service = MarketDataService(session)
        await service.get_prices(symbol="BRENT", limit=1)
        await service.get_prices(symbol="WTI", limit=1)
        await service.get_fundamentals(limit=1)
    return "market_data_refresh_completed"


@celery_app.task(name="app.workers.tasks.refresh_events")
def refresh_events() -> str:
    return asyncio.run(_refresh_events())


async def _refresh_events() -> str:
    async with SessionLocal() as session:
        service = EventService(session)
        await service.get_events(limit=1)
    return "event_refresh_completed"


@celery_app.task(name="app.workers.tasks.evaluate_alerts")
def evaluate_alerts() -> str:
    return asyncio.run(_evaluate_alerts())


async def _evaluate_alerts() -> str:
    async with SessionLocal() as session:
        service = AlertService(session)
        payload = await service.evaluate()
    return f"alerts_evaluated:{payload['triggered_count']}"
