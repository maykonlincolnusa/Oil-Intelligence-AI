from pydantic import BaseModel


class SatelliteSummaryResponse(BaseModel):
    recent_observations: int
    active_fire_events: int
    potential_oil_spills: int
    monitored_storage_sites: int
    monitored_refineries: int
    top_alerts: list[str]
