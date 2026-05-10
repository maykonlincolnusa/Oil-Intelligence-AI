from statistics import mean, pstdev

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import FundamentalIndicator
from app.repositories import EventRepository, FundamentalsRepository, MarketRepository, MaritimeRepository


class RiskScoringService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.event_repo = EventRepository(session)
        self.market_repo = MarketRepository(session)
        self.fund_repo = FundamentalsRepository(session)
        self.maritime_repo = MaritimeRepository(session)

    async def calculate(self) -> dict:
        events = await self.event_repo.get_recent_events(days=14)
        prices = await self.market_repo.get_prices(symbol="BRENT", limit=45)
        crude_inventory = await self.fund_repo.get_fundamentals(
            indicator=FundamentalIndicator.CRUDE_INVENTORY,
            limit=12,
        )
        anomalies = await self.maritime_repo.get_anomalies()

        event_pressure = 0.0
        affected_regions: set[str] = set()
        affected_assets: set[str] = set()
        geopolitical = maritime = supply = demand = refinery = 20.0
        for ev in events:
            confidence = ev.confidence_score
            sentiment_component = max(0.0, ev.sentiment)
            event_pressure += confidence * (1.2 + sentiment_component)
            affected_regions.update(ev.affected_regions or [])
            affected_assets.update(ev.affected_assets or [])

            if "geopolitical_risk" in ev.categories:
                geopolitical += 7 * confidence
            if "maritime_risk" in ev.categories:
                maritime += 7 * confidence
            if "supply_risk" in ev.categories:
                supply += 6 * confidence
            if "demand_risk" in ev.categories:
                demand += 6 * confidence
            if "refinery_risk" in ev.categories:
                refinery += 6 * confidence

        for anomaly in anomalies:
            maritime += anomaly.risk_score / 18

        volatility_score = 0.0
        if len(prices) > 6:
            values = [float(p.value) for p in prices]
            vol = pstdev(values) / max(mean(values), 1e-6)
            volatility_score = min(20.0, vol * 250)

        inventory_direction = 0.0
        if len(crude_inventory) >= 2:
            latest = float(crude_inventory[0].value)
            previous = float(crude_inventory[1].value)
            # Draws are typically bullish and often increase risk sensitivity.
            inventory_direction = 8.0 if latest < previous else -5.0

        geopolitical = self._clamp(geopolitical)
        maritime = self._clamp(maritime + volatility_score * 0.25)
        supply = self._clamp(supply + inventory_direction + volatility_score * 0.2)
        demand = self._clamp(demand + max(0.0, -inventory_direction) * 0.4)
        refinery = self._clamp(refinery + volatility_score * 0.15)

        global_score = self._clamp(
            0.24 * geopolitical
            + 0.2 * maritime
            + 0.2 * supply
            + 0.14 * demand
            + 0.12 * refinery
            + min(15.0, event_pressure)
        )
        global_score_int = int(round(global_score))
        volatility_score_int = int(round(volatility_score))

        return {
            "global_risk_score": global_score_int,
            "geopolitical_risk_score": int(round(geopolitical)),
            "maritime_risk_score": int(round(maritime)),
            "supply_risk_score": int(round(supply)),
            "demand_risk_score": int(round(demand)),
            "refinery_risk_score": int(round(refinery)),
            "volatility_score": volatility_score_int,
            "level": self._level(global_score_int),
            "drivers": [
                f"{len(events)} recent geopolitical/oil events analyzed",
                f"Brent volatility contribution: {volatility_score:.1f}",
                "Inventory direction included in supply stress",
            ],
            "recent_events": [ev.headline for ev in events[:5]],
            "affected_regions": sorted(affected_regions) or ["Global"],
            "affected_assets": sorted(affected_assets) or ["global_crude_market"],
            "confidence": self._confidence(events_count=len(events), prices_count=len(prices)),
            "details": {
                "event_pressure": round(event_pressure, 2),
                "volatility_score": round(volatility_score, 2),
                "inventory_signal": round(inventory_direction, 2),
            },
        }

    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(100.0, value))

    @staticmethod
    def _level(score: int) -> str:
        if score >= 85:
            return "critical"
        if score >= 70:
            return "high"
        if score >= 55:
            return "elevated"
        if score >= 35:
            return "moderate"
        return "low"

    @staticmethod
    def _confidence(events_count: int, prices_count: int) -> float:
        confidence = 0.55 + min(0.25, events_count * 0.025) + min(0.15, prices_count * 0.003)
        return round(min(0.95, confidence), 2)
