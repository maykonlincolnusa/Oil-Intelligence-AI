from datetime import date

from pydantic import BaseModel


class WellProductionOut(BaseModel):
    well_name: str
    period_date: date
    oil_bpd: float
    gas_mmscfd: float | None = None


class FieldSummaryOut(BaseModel):
    field_name: str
    country: str
    basin: str
    operator: str
    active_wells: int
    latest_total_oil_bpd: float


class FieldsSummaryResponse(BaseModel):
    fields: list[FieldSummaryOut]
    production_samples: list[WellProductionOut]
