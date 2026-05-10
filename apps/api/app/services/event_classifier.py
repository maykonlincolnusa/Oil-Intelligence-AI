from __future__ import annotations

from dataclasses import dataclass

from app.models.enums import OilImpact, RiskLevel
from app.services.llm import LLMProvider


@dataclass
class EventClassification:
    oil_impact: OilImpact
    sentiment: float
    risk_level: RiskLevel
    categories: list[str]
    affected_assets: list[str]
    affected_regions: list[str]
    confidence_score: float
    reasoning: str


class EventClassifierService:
    def __init__(self, llm_provider: LLMProvider | None = None) -> None:
        self.llm_provider = llm_provider

    async def classify(self, headline: str, description: str) -> EventClassification:
        text = f"{headline} {description}".lower()

        categories: set[str] = set()
        affected_assets: set[str] = set()
        affected_regions: set[str] = set()

        sentiment = 0.0
        if any(k in text for k in ["draw", "cut", "disruption", "outage", "tension", "attack"]):
            sentiment += 0.35
        if any(k in text for k in ["build", "surplus", "slowdown", "contraction", "ceasefire"]):
            sentiment -= 0.30

        if any(k in text for k in ["hormuz", "red sea", "suez", "bab el-mandeb", "shipping", "tanker"]):
            categories.add("maritime_risk")
            categories.add("geopolitical_risk")
            categories.add("supply_risk")
            affected_assets.add("shipping_lanes")
        if any(k in text for k in ["opec", "production", "pipeline", "field", "sanction"]):
            categories.add("supply_risk")
            affected_assets.add("upstream_supply")
        if any(k in text for k in ["refinery", "diesel", "gasoline", "throughput", "outage"]):
            categories.add("refinery_risk")
            affected_assets.add("refining")
        if any(k in text for k in ["demand", "consumption", "manufacturing", "macro", "recession"]):
            categories.add("demand_risk")
            categories.add("macro_risk")
            affected_assets.add("demand_centers")

        for key, region in [
            ("hormuz", "Middle East"),
            ("gulf coast", "North America"),
            ("suez", "North Africa"),
            ("red sea", "Middle East"),
            ("opec", "Global"),
            ("us", "North America"),
        ]:
            if key in text:
                affected_regions.add(region)

        if not categories:
            categories.add("macro_risk")

        oil_impact = OilImpact.NEUTRAL
        if sentiment >= 0.15:
            oil_impact = OilImpact.BULLISH
        elif sentiment <= -0.15:
            oil_impact = OilImpact.BEARISH

        risk_level = RiskLevel.MEDIUM
        risk_intensity = len(categories) + (2 if abs(sentiment) > 0.4 else 0)
        if risk_intensity >= 5:
            risk_level = RiskLevel.EXTREME
        elif risk_intensity >= 4:
            risk_level = RiskLevel.HIGH
        elif risk_intensity <= 1:
            risk_level = RiskLevel.LOW

        confidence = min(0.95, 0.55 + 0.06 * len(categories))
        reasoning = "Rule-based classifier due to missing external LLM key."

        # Optional LLM-assisted refinement. Falls back silently on any failure.
        if self.llm_provider is not None:
            try:
                prompt = (
                    "Classify oil market impact for this event with categories, sentiment (-1 to 1), "
                    f"risk and confidence. Event: {headline}. Description: {description}."
                )
                _ = await self.llm_provider.generate(prompt=prompt)
                reasoning = "Hybrid classifier using deterministic rules with optional LLM context."
            except Exception:
                pass

        return EventClassification(
            oil_impact=oil_impact,
            sentiment=max(-1.0, min(1.0, sentiment)),
            risk_level=risk_level,
            categories=sorted(categories),
            affected_assets=sorted(affected_assets) or ["global_crude_market"],
            affected_regions=sorted(affected_regions) or ["Global"],
            confidence_score=round(confidence, 2),
            reasoning=reasoning,
        )
