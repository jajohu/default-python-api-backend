from app.services import get_usage


def test_get_usage(mock_report_api, mock_current_period_api):
    report_id = 42
    mock_report_api(cost=10, report_id=report_id)
    mock_current_period_api(report_id)
    usage = get_usage()
    assert len(usage.usage) == 2