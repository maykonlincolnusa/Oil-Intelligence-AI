from datetime import date, timedelta


class VolveProductionLoader:
    async def load_sample(self) -> list[dict]:
        # TODO: parse real Volve-like datasets and map to production entities.
        start = date.today() - timedelta(days=5)
        return [
            {
                "well_name": "VOLVE-01",
                "period_date": start,
                "oil_bpd": 11500.0,
                "gas_mmscfd": 8.2,
            },
            {
                "well_name": "VOLVE-02",
                "period_date": start + timedelta(days=1),
                "oil_bpd": 11120.0,
                "gas_mmscfd": 8.0,
            },
        ]
