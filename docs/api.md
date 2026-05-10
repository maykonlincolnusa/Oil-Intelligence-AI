# API Contract

Oil Intelligence AI uses snake_case JSON keys in backend responses and TypeScript types in the frontend mirror those contracts directly. The frontend API client in `apps/web/lib/api.ts` is the only place that should adapt fetch behavior, fallback data, and endpoint URLs.

## Versioning Strategy

- Legacy compatibility routes remain available under `/api/*`.
- Canonical versioned routes now live under `/api/v1/*`.
- Health endpoints are available at both root and versioned aliases:
  - `/health`, `/health/live`, `/health/ready`
  - `/api/v1/health`, `/api/v1/health/live`, `/api/v1/health/ready`

## Core Endpoints

- `GET /api/v1/market/prices?symbol=BRENT&limit=60&offset=0`
- `GET /api/v1/market/fundamentals?limit=100&offset=0`
- `GET /api/v1/events?limit=20&offset=0`
- `POST /api/v1/events/classify`
- `GET /api/v1/risk/summary`
- `POST /api/v1/scenarios/generate`
- `GET /api/v1/maritime/chokepoints?limit=100&offset=0`
- `GET /api/v1/maritime/vessels?limit=100&offset=0`
- `GET /api/v1/maritime/routes?limit=100&offset=0`
- `GET /api/v1/maritime/risk-summary`
- `GET /api/v1/satellite/summary`
- `GET /api/v1/fields/summary`
- `GET /api/v1/reports/daily`
- `POST /api/v1/reports/generate`
- `GET /api/v1/reports/daily/pdf`
- `GET /api/v1/alerts/rules?limit=100&offset=0`
- `GET /api/v1/alerts/events?limit=100&offset=0`
- `POST /api/v1/alerts/evaluate`

## Pagination Contract (v1)

List endpoints in `/api/v1/*` return:

```json
{
  "items": [],
  "pagination": {
    "total": 0,
    "limit": 100,
    "offset": 0,
    "has_more": false
  }
}
```

Legacy `/api/*` routes preserve previous response shapes for backward compatibility.

## Scenario Request

```json
{
  "scenario_title": "Strait of Hormuz disruption",
  "event_description": "Escalation temporarily disrupts tanker traffic.",
  "affected_region": "Middle East",
  "affected_asset": "Shipping lanes",
  "horizon_days": 30,
  "severity": "high"
}
```

For backward compatibility, the backend also accepts `title` as an alias for `scenario_title`.

## Risk Summary Response

`GET /api/v1/risk/summary` returns explainable scoring fields:

- `global_risk_score`
- `geopolitical_risk_score`
- `maritime_risk_score`
- `supply_risk_score`
- `demand_risk_score`
- `refinery_risk_score`
- `volatility_score`
- `level`
- `drivers`
- `recent_events`
- `affected_regions`
- `affected_assets`
- `confidence`

## Mock Mode

External API keys are optional. When keys are missing, connectors return seeded or deterministic sample data so the app remains usable locally.
