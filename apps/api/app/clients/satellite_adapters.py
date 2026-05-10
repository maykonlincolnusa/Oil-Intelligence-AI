from datetime import datetime, timezone


class SentinelHubAdapter:
    async def fetch_storage_activity(self) -> list[dict]:
        # TODO: connect Sentinel Hub imagery APIs.
        return [
            {
                "provider": "Sentinel Hub",
                "observed_at": datetime.now(timezone.utc),
                "observation_type": "storage_tank_fill_estimate",
                "summary": "Sample storage tank fill changes detected over key terminals.",
                "confidence_score": 0.62,
            }
        ]


class NASAFirmsAdapter:
    async def fetch_fire_alerts(self) -> list[dict]:
        # TODO: connect NASA FIRMS feeds.
        return [
            {
                "site_name": "Gulf Coast Refinery Cluster",
                "intensity": 0.8,
                "confidence_score": 0.74,
            }
        ]


class CommercialSatelliteAdapter:
    async def fetch_refinery_signals(self) -> list[dict]:
        # TODO: integrate commercial satellite providers for higher frequency revisits.
        return [
            {
                "provider": "Commercial SAT Mock",
                "signal": "flare_intensity",
                "summary": "Elevated flare intensity suggests transient throughput changes.",
            }
        ]
