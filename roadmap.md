# Roadmap

## Phase 0 - MVP (Completed)

- Monorepo architecture with backend/frontend separation
- Core modules: market, fundamentals, events, risk, scenarios
- Maritime/satellite/field placeholders with APIs
- Docker Compose runtime, seed data, CI baseline

## Phase 1 - Production Readiness

- AuthN/AuthZ (OIDC, role-based access)
- Alembic migration policy and release process
- Distributed tracing and metrics
- Redis caching strategy hardening

## Phase 1 - Delivered Scope (May 2026)

- API versioning with `/api/v1` and legacy compatibility aliases.
- Standardized pagination metadata for v1 list endpoints.
- Structured request logging with request IDs.
- Liveness/readiness probes with Postgres/Redis dependency checks.
- Celery beat cadence for market/event refresh and alert evaluation.

## Phase 2 - Live Intelligence Integrations

- Real EIA/FRED/GDELT connectors
- Real-time AIS ingestion and route anomaly engine
- Satellite pipeline for fire/flare/storage observations
- Multi-source event fusion and confidence calibration

## Phase 3 - Advanced Analytics

- Regime-aware risk scoring models
- Forecasting (price/fundamentals) with backtesting
- Scenario engine with probabilistic outputs
- RAG-enabled analyst copilot on internal research corpus

## Phase 4 - Enterprise Platform

- Multi-tenant architecture and workspace isolation
- Fine-grained data entitlements
- Audit trails and governance controls
- SLA-backed deployment and incident response runbooks

## Stretch Vision

- Full OSDU/WITSML interoperability
- Field-level digital twin with production optimization analytics
- Satellite + maritime + macro fusion for early warning intelligence
