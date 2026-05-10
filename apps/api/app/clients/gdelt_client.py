from datetime import datetime, timedelta, timezone


class GDELTClient:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key

    async def fetch_oil_news_events(self) -> list[dict]:
        # TODO: integrate GDELT API and article scraping pipeline.
        now = datetime.now(timezone.utc)
        return [
            {
                "event_time": now - timedelta(hours=5),
                "headline": "Tensions rise near Strait of Hormuz after naval incident",
                "description": "Shipping operators reported temporary rerouting of crude tankers.",
                "source": "GDELT_MOCK",
            },
            {
                "event_time": now - timedelta(hours=11),
                "headline": "Unplanned refinery outage impacts diesel output in Gulf Coast",
                "description": "A major refinery entered emergency maintenance and reduced runs.",
                "source": "GDELT_MOCK",
            },
            {
                "event_time": now - timedelta(days=1),
                "headline": "Larger-than-expected U.S. crude inventory draw",
                "description": "Weekly data showed a drawdown supporting stronger prompt pricing.",
                "source": "GDELT_MOCK",
            },
            {
                "event_time": now - timedelta(days=2),
                "headline": "Manufacturing contraction raises concerns on oil demand outlook",
                "description": "Macro data signaled weaker fuel demand growth over next quarter.",
                "source": "GDELT_MOCK",
            },
        ]
