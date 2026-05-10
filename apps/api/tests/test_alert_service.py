from app.services.alert_service import AlertService


def test_alert_comparator_rules() -> None:
    assert AlertService._evaluate_comparator(4.0, ">", 3.0) is True
    assert AlertService._evaluate_comparator(3.0, ">", 3.0) is False
    assert AlertService._evaluate_comparator(3.0, ">=", 3.0) is True
    assert AlertService._evaluate_comparator(2.0, "<", 3.0) is True
