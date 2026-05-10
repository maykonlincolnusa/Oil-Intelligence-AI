# Roadmap

## Current MVP

- Market data and petroleum fundamentals APIs.
- Event classification with deterministic fallback.
- Explainable risk scoring.
- Scenario generation.
- Maritime, satellite, and reservoir placeholders.
- Daily report generation and PDF export.
- Alert rules and alert event history.

## Next Engineering Milestones

- Replace `AUTO_CREATE_TABLES` in production with Alembic-only migrations.
- Add auth, workspace isolation, and role-based permissions.

## Recently Completed (May 2026)

- Added API version prefix (`/api/v1`) while keeping current routes as compatibility aliases.
- Added structured logging and request IDs.
- Added pagination metadata for list endpoints in v1.
- Added scheduled ingestion/evaluation jobs via Celery beat.
- Added readiness and liveness health probes.

## Intelligence Milestones

- Real EIA/FRED/GDELT connector implementations.
- AIS provider adapter and route anomaly scoring.
- Satellite alert ingestion with provider provenance.
- RAG-backed analyst briefings using pgvector.
- Backtested risk scoring and calibration reports.
