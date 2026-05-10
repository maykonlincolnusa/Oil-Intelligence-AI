from fastapi import APIRouter

from app.api.routes.alerts import router as alerts_router
from app.api.routes.events import router as events_router
from app.api.routes.fields import router as fields_router
from app.api.routes.health import router as health_router
from app.api.routes.maritime import router as maritime_router
from app.api.routes.market import router as market_router
from app.api.routes.reports import router as reports_router
from app.api.routes.risk import router as risk_router
from app.api.routes.scenarios import router as scenarios_router
from app.api.routes.satellite import router as satellite_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(market_router)
api_router.include_router(events_router)
api_router.include_router(risk_router)
api_router.include_router(alerts_router)
api_router.include_router(reports_router)
api_router.include_router(scenarios_router)
api_router.include_router(maritime_router)
api_router.include_router(satellite_router)
api_router.include_router(fields_router)
