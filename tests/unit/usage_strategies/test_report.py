import datetime

import pytest
from app.exceptions import ReportNotFound
from app.models.message import Message
from app.usage_strategies.report import ReportUsageStrategy


def test_report_usage_strategy(mock_report_api):
    expected_cost = 10
    report_id = 42
    mock_report_api(cost=expected_cost, report_id=report_id)
    strategy = ReportUsageStrategy()
    assert (
        strategy.calculate_usage(
            Message(
                text="report please",
                timestamp=datetime.datetime(2024, 1, 1, 0, 0, 0),
                id=3,
                report_id=report_id,
            )
        ).usage
        == expected_cost
    )


def test_report_usage_strategy_404(mock_report_api):
    report_id = 999
    mock_report_api(cost=0, report_id=report_id, status_code=404)

    strategy = ReportUsageStrategy()
    message = Message(
        text="report please",
        timestamp=datetime.datetime(2024, 1, 1, 0, 0, 0),
        id=3,
        report_id=report_id,
    )

    with pytest.raises(ReportNotFound) as exc_info:
        strategy.calculate_usage(message)

    assert str(exc_info.value) == f"Could not find report ID {report_id}"
