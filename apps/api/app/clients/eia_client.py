from datetime import datetime, timedelta, timezone
from random import uniform


class EIAClient:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key

    async def get_crude_prices(self, symbol: str = "BRENT", days: int = 30) -> list[dict]:
        # TODO: integrate real EIA series endpoints when API key is configured.
        now = datetime.now(timezone.utc)
        base_price = 82.0 if symbol.upper() == "BRENT" else 78.0
        series: list[dict] = []
        for i in range(days):
            ts = now - timedelta(days=days - i)
            close = base_price + uniform(-2.8, 2.8)
            series.append(
                {
                    "symbol": symbol.upper(),
                    "timestamp": ts,
                    "open": close - uniform(0.3, 1.2),
                    "high": close + uniform(0.2, 1.4),
                    "low": close - uniform(0.2, 1.4),
                    "close": close,
                    "value": close,
                    "source": "EIA_MOCK" if not self.api_key else "EIA",
                    "metadata": {"mock": self.api_key is None},
                }
            )
        return series
