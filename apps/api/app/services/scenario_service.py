from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import Severity
from app.models.scenario import Scenario
from app.services.llm import get_llm_provider


class ScenarioService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.llm = get_llm_provider()

    async def generate(
        self,
        title: str,
        event_description: str,
        affected_region: str,
        affected_asset: str,
        horizon_days: int,
        severity: str,
    ) -> dict:
        sev = severity.lower()
        severity_factor = {
            "low": 0.45,
            "medium": 0.58,
            "high": 0.72,
            "extreme": 0.84,
        }.get(sev, 0.58)

        executive_summary = (
            f"{title} scenario for {affected_region} over {horizon_days} days suggests "
            f"elevated monitoring of {affected_asset} with {sev} severity conditions."
        )
        base_case = (
            "Base case assumes partial disruption with adaptive rerouting and gradual market "
            "normalization after initial risk premium expansion."
        )
        bullish_case = (
            "Bullish case for oil: prolonged disruption tightens prompt supply, lifts front-month "
            "crude spreads, and supports refining margins in unaffected regions."
        )
        bearish_case = (
            "Bearish case for oil: disruption resolves quickly, inventories rebuild, and macro headwinds "
            "cap demand growth, pressuring crude benchmarks lower."
        )
        operational_impact = (
            "Expected impacts include shipping delays, feedstock procurement repricing, increased "
            "working capital needs, and higher optionality value for storage and blending assets."
        )

        sectors = [
            "Upstream Producers",
            "Refiners",
            "Shipping & Logistics",
            "Commodity Trading Houses",
            "Airlines & Heavy Industry",
        ]
        monitoring_signals = [
            "Brent-WTI spread",
            "Freight rates through key chokepoints",
            "Weekly crude and product inventories",
            "Refinery utilization changes",
            "Official policy and sanctions announcements",
        ]
        risk_drivers = self._risk_drivers(title=title, description=event_description, severity=sev)
        price_pressure = self._price_pressure(severity=sev, description=event_description)
        disclaimer = (
            "This scenario is for market intelligence and operational planning only. "
            "It is not financial, trading, or investment advice."
        )

        prompt = (
            "Enhance this oil scenario analysis into concise institutional language. "
            f"Title: {title}. Event: {event_description}. Region: {affected_region}."
        )
        try:
            ai_text = await self.llm.generate(prompt=prompt)
            if ai_text:
                executive_summary = f"{executive_summary} {ai_text[:220]}"
        except Exception:
            pass

        confidence = round(min(0.95, severity_factor + 0.05), 2)

        scenario = Scenario(
            title=title,
            event_description=event_description,
            affected_region=affected_region,
            affected_asset=affected_asset,
            horizon_days=horizon_days,
            severity=Severity(sev),
            executive_summary=executive_summary,
            base_case=base_case,
            bullish_case=bullish_case,
            bearish_case=bearish_case,
            operational_impact=operational_impact,
            affected_sectors=sectors,
            confidence=confidence,
            recommended_monitoring_signals=monitoring_signals,
            metadata_json={"generated_by": "scenario_engine_v1"},
        )
        self.session.add(scenario)
        await self.session.commit()

        return {
            "executive_summary": executive_summary,
            "base_case": base_case,
            "bullish_case": bullish_case,
            "bearish_case": bearish_case,
            "operational_impact": operational_impact,
            "affected_sectors": sectors,
            "price_pressure": price_pressure,
            "risk_drivers": risk_drivers,
            "monitoring_signals": monitoring_signals,
            "confidence": confidence,
            "disclaimer": disclaimer,
            "recommended_monitoring_signals": monitoring_signals,
        }

    @staticmethod
    def _risk_drivers(title: str, description: str, severity: str) -> list[str]:
        text = f"{title} {description}".lower()
        drivers = [f"{severity.title()} severity event path"]
        if any(term in text for term in ["hormuz", "suez", "red sea", "tanker", "shipping"]):
            drivers.append("Chokepoint transit risk")
            drivers.append("Freight and war-risk premium")
        if any(term in text for term in ["opec", "production", "cut", "sanction"]):
            drivers.append("Supply availability risk")
        if any(term in text for term in ["refinery", "diesel", "gasoline", "outage"]):
            drivers.append("Refinery throughput and product crack risk")
        if any(term in text for term in ["inventory", "drawdown", "storage"]):
            drivers.append("Inventory buffer compression")
        if any(term in text for term in ["china", "demand", "slowdown", "macro"]):
            drivers.append("Demand-side macro sensitivity")
        return sorted(set(drivers))

    @staticmethod
    def _price_pressure(severity: str, description: str) -> str:
        bearish_terms = ["slowdown", "demand", "recession", "build", "surplus"]
        if any(term in description.lower() for term in bearish_terms):
            return "bearish"
        if severity in {"high", "extreme"}:
            return "strongly_bullish"
        if severity == "medium":
            return "moderately_bullish"
        return "neutral_to_slightly_bullish"
