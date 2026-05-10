from app.services.risk_scoring_service import RiskScoringService


def test_risk_level_boundaries() -> None:
    assert RiskScoringService._level(90) == "critical"
    assert RiskScoringService._level(72) == "high"
    assert RiskScoringService._level(58) == "elevated"
    assert RiskScoringService._level(40) == "moderate"
    assert RiskScoringService._level(20) == "low"
