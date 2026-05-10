from datetime import date, datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import FundamentalIndicator
from app.models.risk import DailyIntelligenceReport
from app.repositories import EventRepository, MarketRepository
from app.services.llm import get_llm_provider
from app.services.maritime_service import MaritimeService
from app.services.risk_scoring_service import RiskScoringService
from app.services.satellite_service import SatelliteService


class ReportService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.market_repo = MarketRepository(session)
        self.event_repo = EventRepository(session)
        self.risk_service = RiskScoringService(session)
        self.maritime_service = MaritimeService(session)
        self.satellite_service = SatelliteService(session)
        self.llm = get_llm_provider()

    async def generate_daily_report(self, report_date: date | None = None) -> dict:
        report_date = report_date or date.today()

        brent = await self.market_repo.get_prices(symbol="BRENT", limit=2)
        wti = await self.market_repo.get_prices(symbol="WTI", limit=2)
        events = await self.event_repo.get_events(limit=10)
        risk = await self.risk_service.calculate()
        maritime = await self.maritime_service.risk_summary()
        satellite = await self.satellite_service.summary()
        crude_inventory = await self.risk_service.fund_repo.get_fundamentals(
            indicator=FundamentalIndicator.CRUDE_INVENTORY,
            limit=2,
        )

        movers = []
        for symbol, rows in [("BRENT", brent), ("WTI", wti)]:
            if len(rows) < 2:
                continue
            latest = float(rows[0].value)
            prev = float(rows[1].value)
            change = ((latest - prev) / prev) * 100 if prev else 0.0
            movers.append(
                {
                    "symbol": symbol,
                    "last_price": round(latest, 2),
                    "change_percent": round(change, 2),
                }
            )

        top_events = [
            {
                "headline": ev.headline,
                "risk_level": str(ev.risk_level),
                "oil_impact": str(ev.oil_impact),
                "confidence_score": round(ev.confidence_score, 2),
            }
            for ev in events[:5]
        ]

        refinery_storage_alerts = []
        if satellite["active_fire_events"] > 0:
            refinery_storage_alerts.append(
                f"{satellite['active_fire_events']} fire/thermal refinery alerts detected"
            )
        if satellite["potential_oil_spills"] > 0:
            refinery_storage_alerts.append(
                f"{satellite['potential_oil_spills']} potential spill observations require validation"
            )
        if not refinery_storage_alerts:
            refinery_storage_alerts.append("No critical refinery/storage alerts in latest cycle")

        scenario_watchlist = self._build_scenario_watchlist(top_events)

        market_summary = self._build_market_summary(movers, risk)
        brent_wti_summary = self._build_brent_wti_summary(movers)
        fundamentals_summary = self._build_fundamentals_summary(crude_inventory)
        top_risk_drivers = risk["drivers"][:5]
        executive_summary = await self._build_executive_summary(
            market_summary=market_summary,
            top_events=top_events,
            risk=risk,
            maritime=maritime,
        )
        disclaimer = (
            "This report is generated from mock/sample and configured data sources for intelligence "
            "workflow demonstration. It is not financial, trading, or investment advice."
        )

        report_payload = {
            "report_date": report_date,
            "market_summary": market_summary,
            "brent_wti_summary": brent_wti_summary,
            "top_price_movers": movers,
            "top_geopolitical_events": top_events,
            "top_risk_drivers": top_risk_drivers,
            "fundamentals_summary": fundamentals_summary,
            "risk_score": risk["global_risk_score"],
            "maritime_risk_score": maritime["maritime_risk_score"],
            "refinery_storage_alerts": refinery_storage_alerts,
            "scenario_watchlist": scenario_watchlist,
            "ai_analyst_conclusion": executive_summary,
            "disclaimer": disclaimer,
            "executive_summary": executive_summary,
            "confidence": self._confidence_score(risk["global_risk_score"], len(top_events)),
            "generated_at": datetime.now(timezone.utc),
        }

        existing = await self.session.scalar(
            select(DailyIntelligenceReport).where(DailyIntelligenceReport.report_date == report_date)
        )
        if existing:
            existing.market_summary = report_payload["market_summary"]
            existing.top_price_movers = report_payload["top_price_movers"]
            existing.top_geopolitical_events = report_payload["top_geopolitical_events"]
            existing.risk_score = report_payload["risk_score"]
            existing.maritime_risk_score = report_payload["maritime_risk_score"]
            existing.refinery_storage_alerts = report_payload["refinery_storage_alerts"]
            existing.scenario_watchlist = report_payload["scenario_watchlist"]
            existing.executive_summary = report_payload["executive_summary"]
            existing.confidence = report_payload["confidence"]
            existing.metadata_json = {"source": "daily_report_engine"}
        else:
            self.session.add(
                DailyIntelligenceReport(
                    report_date=report_payload["report_date"],
                    market_summary=report_payload["market_summary"],
                    top_price_movers=report_payload["top_price_movers"],
                    top_geopolitical_events=report_payload["top_geopolitical_events"],
                    risk_score=report_payload["risk_score"],
                    maritime_risk_score=report_payload["maritime_risk_score"],
                    refinery_storage_alerts=report_payload["refinery_storage_alerts"],
                    scenario_watchlist=report_payload["scenario_watchlist"],
                    executive_summary=report_payload["executive_summary"],
                    confidence=report_payload["confidence"],
                    metadata_json={"source": "daily_report_engine"},
                )
            )

        await self.session.commit()
        return report_payload

    def _build_market_summary(self, movers: list[dict], risk: dict) -> str:
        if not movers:
            return "Market data sparse; no significant benchmark mover available."
        mover_text = ", ".join(
            f"{m['symbol']} {m['change_percent']:+.2f}% at {m['last_price']}" for m in movers
        )
        return (
            f"Benchmark performance: {mover_text}. "
            f"Composite risk remains at {risk['global_risk_score']} with elevated attention on "
            f"geopolitical ({risk['geopolitical_risk_score']}) and maritime ({risk['maritime_risk_score']}) vectors."
        )

    @staticmethod
    def _build_brent_wti_summary(movers: list[dict]) -> str:
        by_symbol = {m["symbol"]: m for m in movers}
        brent = by_symbol.get("BRENT")
        wti = by_symbol.get("WTI")
        if not brent or not wti:
            return "Brent/WTI spread summary unavailable until both benchmark series have at least two observations."
        spread = brent["last_price"] - wti["last_price"]
        return (
            f"Brent is {brent['last_price']:.2f}, WTI is {wti['last_price']:.2f}, "
            f"with Brent-WTI spread at {spread:.2f}. Daily benchmark moves are "
            f"{brent['change_percent']:+.2f}% and {wti['change_percent']:+.2f}%."
        )

    @staticmethod
    def _build_fundamentals_summary(crude_inventory: list) -> str:
        if len(crude_inventory) < 2:
            return "Fundamentals summary unavailable until inventory series has at least two observations."
        latest = float(crude_inventory[0].value)
        previous = float(crude_inventory[1].value)
        delta = latest - previous
        direction = "build" if delta > 0 else "draw"
        return f"Crude inventories show a {abs(delta):.2f} mbbl {direction}, latest level {latest:.2f} mbbl."

    async def _build_executive_summary(
        self,
        market_summary: str,
        top_events: list[dict],
        risk: dict,
        maritime: dict,
    ) -> str:
        event_headlines = "; ".join(e["headline"] for e in top_events[:3])
        fallback = (
            f"Daily intelligence view: {market_summary} Key events: {event_headlines}. "
            f"Maritime risk score is {maritime['maritime_risk_score']} and global risk is {risk['global_risk_score']}."
        )

        prompt = (
            "Produce a concise executive oil market briefing (3-4 sentences). "
            f"Market: {market_summary} Events: {event_headlines}. Risk={risk['global_risk_score']}."
        )
        try:
            generated = await self.llm.generate(prompt=prompt)
            if generated and not generated.startswith("Deterministic AI placeholder"):
                return generated[:1200]
        except Exception:
            pass
        return fallback

    @staticmethod
    def _build_scenario_watchlist(top_events: list[dict]) -> list[str]:
        watchlist = [
            "Strait of Hormuz disruption",
            "OPEC+ coordinated production cut",
            "Red Sea shipping disruption",
        ]
        for item in top_events:
            headline = item["headline"].lower()
            if "refinery" in headline:
                watchlist.append("Major refinery outage stress test")
            if "inventory" in headline:
                watchlist.append("US crude drawdown continuation")
            if "hurricane" in headline or "storm" in headline:
                watchlist.append("Gulf of Mexico hurricane impact")
        return sorted(set(watchlist))

    @staticmethod
    def _confidence_score(global_risk: int, top_events_count: int) -> float:
        confidence = 0.58 + min(0.25, top_events_count * 0.04) + min(0.1, global_risk / 1000)
        return round(min(0.95, confidence), 2)
