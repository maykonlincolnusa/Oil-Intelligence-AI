from app.services.report_service import ReportService


def test_report_watchlist_includes_templates() -> None:
    watchlist = ReportService._build_scenario_watchlist(
        [
            {
                "headline": "Refinery outage in Gulf Coast",
                "risk_level": "high",
                "oil_impact": "bullish",
                "confidence_score": 0.8,
            }
        ]
    )

    assert "Strait of Hormuz disruption" in watchlist
    assert "Major refinery outage stress test" in watchlist


def test_report_benchmark_summary() -> None:
    summary = ReportService._build_brent_wti_summary(
        [
            {"symbol": "BRENT", "last_price": 84.2, "change_percent": 1.2},
            {"symbol": "WTI", "last_price": 80.1, "change_percent": 0.8},
        ]
    )

    assert "Brent-WTI spread" in summary
