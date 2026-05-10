from contextlib import asynccontextmanager
import logging
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.core.database import SessionLocal, engine
from app.core.logging import setup_logging
from app.core.request_context import reset_request_id, set_request_id
from app.models import Base
from app.seed.seed_data import run_seed
from app.services.alert_service import AlertService

setup_logging()
settings = get_settings()
logger = logging.getLogger("app.http")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if settings.auto_create_tables:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        await run_seed(session)
        alert_service = AlertService(session)
        await alert_service.ensure_default_rules()

    yield


app = FastAPI(
    title="Oil Intelligence AI API",
    version="0.1.0",
    description="AI-powered oil market intelligence backend",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_middleware(request: Request, call_next):
    request_id = request.headers.get(settings.request_id_header) or uuid4().hex
    token = set_request_id(request_id)
    started_at = perf_counter()
    response = None
    try:
        response = await call_next(request)
        response.headers[settings.request_id_header] = request_id
        return response
    finally:
        duration_ms = round((perf_counter() - started_at) * 1000, 2)
        status_code = response.status_code if response is not None else 500
        logger.info(
            "request_complete",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": status_code,
                "duration_ms": duration_ms,
                "client_ip": request.client.host if request.client else None,
            },
        )
        reset_request_id(token)


app.include_router(api_router)
app.include_router(api_v1_router)
