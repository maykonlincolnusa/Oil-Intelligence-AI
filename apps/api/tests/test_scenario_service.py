from app.services.scenario_service import ScenarioService


def test_scenario_risk_drivers_for_maritime_event() -> None:
    drivers = ScenarioService._risk_drivers(
        title="Strait of Hormuz disruption",
        description="Tankers reroute after shipping disruption",
        severity="high",
    )

    assert "Chokepoint transit risk" in drivers
    assert "Freight and war-risk premium" in drivers


def test_scenario_price_pressure_for_demand_slowdown() -> None:
    pressure = ScenarioService._price_pressure(
        severity="high",
        description="China demand slowdown pressures crude balances",
    )

    assert pressure == "bearish"
