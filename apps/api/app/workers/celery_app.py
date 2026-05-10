import asyncio

from celery import Celery

from app.core.config import get_settings

settings = get_settings()
celery_app = Celery("oil_intelligence", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    imports=("app.workers.tasks",),
    beat_schedule={
        "refresh-market-data": {
            "task": "app.workers.tasks.refresh_market_data",
            "schedule": settings.celery_market_refresh_minutes * 60,
        },
        "refresh-events": {
            "task": "app.workers.tasks.refresh_events",
            "schedule": settings.celery_events_refresh_minutes * 60,
        },
        "evaluate-alerts": {
            "task": "app.workers.tasks.evaluate_alerts",
            "schedule": settings.celery_alerts_refresh_minutes * 60,
        },
    },
)


@celery_app.task
def ping() -> str:
    return "pong"


@celery_app.task
def run_async_task(task_name: str) -> str:
    asyncio.run(asyncio.sleep(0.01))
    return f"completed:{task_name}"
