# Data Sources

## Implemented in MVP (Mock-capable)

### Market Data

- EIA client (`app/clients/eia_client.py`)
- FRED client (`app/clients/fred_client.py`)

If API keys are missing, deterministic sample data is generated.

### News & Events

- GDELT client (`app/clients/gdelt_client.py`)

Mock geopolitical/oil events are returned when no live integration is configured.

### Satellite/Remote Sensing (Placeholders)

- Sentinel Hub adapter
- NASA FIRMS adapter
- Commercial satellite adapter

Current implementation is interface-first with synthetic outputs.

### Reservoir/Field

- Volve-style production loader placeholder

Provides sample production points and a future entrypoint for real datasets.

## Future Integrations

- ICE/CME market data
- OPEC/JODI/OilX style fundamentals
- AIS vessel feeds (exactEarth/Spire/MarineTraffic)
- SAR + optical satellite products for tank/storage inference
- OSDU/WITSML well and production datasets
- Macro datasets (PMI, rates, industrial output)

## Data Quality Principles

- Source attribution on each record (`source`)
- `metadata_json` for provenance and parser notes
- Confidence scoring for AI-classified events
- Clear mock-vs-live mode behavior for deterministic reproducibility

## Recommended Governance Additions (Roadmap)

- Source reliability scoring
- Unit normalization registry
- Region/asset ontology
- Ingestion lineage and versioning
- Event deduplication and entity resolution pipeline

## Derived Intelligence Outputs

- Daily AI intelligence report (`/api/reports/daily`) combining market/event/risk/maritime/satellite signals
- Exportable PDF briefings (`/api/reports/daily/pdf`) for executive distribution
- Rule-based operational alert engine (`/api/alerts/*`) for threshold and event triggers
