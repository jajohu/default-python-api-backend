from app.services import get_usage


def test_get_usage(mock_current_period_api):
    report_id = 42
    mock_current_period_api(report_id)
    usage = get_usage()
    assert len(usage.usage) == 2
