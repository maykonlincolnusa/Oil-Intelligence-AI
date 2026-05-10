from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import FieldRepository


class FieldService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = FieldRepository(session)

    async def summary(self) -> dict:
        fields = await self.repo.list_fields()
        field_items: list[dict] = []
        for field in fields:
            active_wells = await self.repo.active_well_count(field.id)
            total_oil = await self.repo.latest_production_total(field.id)
            field_items.append(
                {
                    "field_name": field.name,
                    "country": field.country,
                    "basin": field.basin,
                    "operator": field.operator,
                    "active_wells": active_wells,
                    "latest_total_oil_bpd": round(total_oil, 2),
                }
            )

        samples = await self.repo.production_samples(limit=20)
        sample_payload = [
            {
                "well_name": well_name,
                "period_date": prod.period_date,
                "oil_bpd": prod.oil_bpd,
                "gas_mmscfd": prod.gas_mmscfd,
            }
            for well_name, prod in samples
        ]

        return {"fields": field_items, "production_samples": sample_payload}
