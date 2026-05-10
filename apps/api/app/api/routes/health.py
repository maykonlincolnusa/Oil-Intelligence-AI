from datetime import datetime, timezone
from time import perf_counter

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.core.config import get_settings
from app.schemas.health import DependencyHealth, HealthResponse, ReadinessResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", service="oil-intelligence-api", environment=settings.api_env)


@router.get("/health/live", response_model=HealthResponse)
async def health_live() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", service="oil-intelligence-api", environment=settings.api_env)


@router.get("/health/ready", response_model=ReadinessResponse)
async def health_ready(session: AsyncSession = Depends(get_session)) -> JSONResponse:
    settings = get_settings()
    dependencies = [
        await _check_database(session),
        await _check_redis(settings.redis_url),
    ]

    status_value = "ok" if all(dep.status == "ok" for dep in dependencies) else "degraded"
    payload = ReadinessResponse(
        status=status_value,
        service="oil-intelligence-api",
        environment=settings.api_env,
        checked_at=datetime.now(timezone.utc),
        dependencies=dependencies,
    )

    status_code = (
        status.HTTP_200_OK
        if status_value == "ok"
        else status.HTTP_503_SERVICE_UNAVAILABLE
    )
    return JSONResponse(status_code=status_code, content=payload.model_dump(mode="json"))


async def _check_database(session: AsyncSession) -> DependencyHealth:
    started_at = perf_counter()
    try:
        await session.execute(text("SELECT 1"))
        return DependencyHealth(
            name="postgres",
            status="ok",
            latency_ms=round((perf_counter() - started_at) * 1000, 2),
        )
    except Exception as exc:
        return DependencyHealth(
            name="postgres",
            status="error",
            latency_ms=round((perf_counter() - started_at) * 1000, 2),
            detail=str(exc),
        )


async def _check_redis(redis_url: str) -> DependencyHealth:
    started_at = perf_counter()
    client = Redis.from_url(redis_url, decode_responses=True)
    try:
        await client.ping()
        return DependencyHealth(
            name="redis",
            status="ok",
            latency_ms=round((perf_counter() - started_at) * 1000, 2),
        )
    except Exception as exc:
        return DependencyHealth(
            name="redis",
            status="error",
            latency_ms=round((perf_counter() - started_at) * 1000, 2),
            detail=str(exc),
        )
    finally:
        await client.aclose()
