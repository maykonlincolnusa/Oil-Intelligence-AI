import pytest

from app.services.event_classifier import EventClassifierService


@pytest.mark.asyncio
async def test_event_classifier_detects_maritime_and_supply_risk() -> None:
    svc = EventClassifierService()
    result = await svc.classify(
        headline="Incident near Strait of Hormuz",
        description="Tanker rerouting raises supply disruption concerns",
    )

    assert "maritime_risk" in result.categories
    assert "supply_risk" in result.categories
    assert result.sentiment > 0
    assert result.confidence_score >= 0.55
