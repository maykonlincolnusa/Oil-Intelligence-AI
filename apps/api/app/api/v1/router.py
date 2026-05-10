from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.v1.routes.alerts import router as alerts_router
from app.api.v1.routes.events import router as events_router
from app.api.v1.routes.fields import router as fields_router
from app.api.v1.routes.maritime import router as maritime_router
from app.api.v1.routes.market import router as market_router
from app.api.v1.routes.reports import router as reports_router
from app.api.v1.routes.risk import router as risk_router
from app.api.v1.routes.satellite import router as satellite_router
from app.api.v1.routes.scenarios import router as scenarios_router
from app.core.config import get_settings

settings = get_settings()
api_v1_router = APIRouter(prefix=settings.api_version_prefix)

api_v1_router.include_router(health_router)
api_v1_router.include_router(market_router)
api_v1_router.include_router(events_router)
api_v1_router.include_router(risk_router)
api_v1_router.include_router(alerts_router)
api_v1_router.include_router(reports_router)
api_v1_router.include_router(scenarios_router)
api_v1_router.include_router(maritime_router)
api_v1_router.include_router(satellite_router)
api_v1_router.include_router(fields_router)
