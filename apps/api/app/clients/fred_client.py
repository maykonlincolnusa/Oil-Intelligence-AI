from datetime import date, timedelta
from random import uniform

from app.models.enums import FundamentalIndicator


class FREDClient:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key

    async def get_fundamentals(self, days: int = 30) -> list[dict]:
        # TODO: integrate real FRED series mapping for global oil indicators.
        today = date.today()
        indicators = [
            FundamentalIndicator.CRUDE_INVENTORY,
            FundamentalIndicator.GASOLINE_INVENTORY,
            FundamentalIndicator.DISTILLATE_INVENTORY,
            FundamentalIndicator.REFINERY_UTILIZATION,
            FundamentalIndicator.PRODUCTION,
            FundamentalIndicator.IMPORTS,
            FundamentalIndicator.EXPORTS,
            FundamentalIndicator.CONSUMPTION,
        ]
        rows: list[dict] = []
        for i in range(days):
            period = today - timedelta(days=days - i)
            for ind in indicators:
                value = {
                    FundamentalIndicator.CRUDE_INVENTORY: 440 + uniform(-12, 12),
                    FundamentalIndicator.GASOLINE_INVENTORY: 230 + uniform(-8, 8),
                    FundamentalIndicator.DISTILLATE_INVENTORY: 118 + uniform(-6, 6),
                    FundamentalIndicator.REFINERY_UTILIZATION: 89 + uniform(-3, 3),
                    FundamentalIndicator.PRODUCTION: 13 + uniform(-0.6, 0.6),
                    FundamentalIndicator.IMPORTS: 6.5 + uniform(-0.7, 0.7),
                    FundamentalIndicator.EXPORTS: 4.2 + uniform(-0.6, 0.6),
                    FundamentalIndicator.CONSUMPTION: 20 + uniform(-1.0, 1.0),
                }[ind]
                unit = "mbbl" if "inventory" in ind else "mbpd"
                if ind == FundamentalIndicator.REFINERY_UTILIZATION:
                    unit = "percent"
                rows.append(
                    {
                        "indicator": ind,
                        "country": "United States",
                        "region": "North America",
                        "product_type": "crude" if "inventory" in ind else "petroleum",
                        "unit": unit,
                        "period": period,
                        "value": value,
                        "source": "FRED_MOCK" if not self.api_key else "FRED",
                        "metadata": {"mock": self.api_key is None},
                    }
                )
        return rows
