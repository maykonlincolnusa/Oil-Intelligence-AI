# Data Sources

The MVP runs without paid APIs. Each connector is structured so a real provider can replace mock behavior later.

## Implemented Connectors

- EIA mock client for crude benchmark time series.
- FRED mock client for petroleum fundamentals.
- GDELT mock client for geopolitical and oil-relevant event samples.
- Sentinel Hub adapter placeholder for storage/refinery observations.
- NASA FIRMS adapter placeholder for fire event monitoring.
- Commercial satellite adapter placeholder for higher frequency remote sensing feeds.
- Volve-style loader placeholder for well production datasets.

## Future Provider Targets

- Market/fundamentals: EIA, FRED, JODI, OPEC, exchange or vendor feeds.
- Maritime: Spire, Kpler, Vortexa, MarineTraffic, VesselFinder, AIS aggregators.
- Satellite: Sentinel Hub, NASA FIRMS, Planet, Maxar, ICEYE, Capella.
- Upstream: OSDU, WITSML, public Volve-style datasets, internal production systems.

## Governance Principles

- Every record keeps source metadata.
- Mock data is explicitly identified by source or metadata.
- Units and regions should be normalized before introducing real providers.
- Entity resolution should be added before mixing multiple live news or AIS feeds.
