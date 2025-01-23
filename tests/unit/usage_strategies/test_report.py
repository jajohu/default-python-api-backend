import datetime
from app.models.message import Message
from app.usage_strategies.report import ReportUsageStrategy


def test_report_usage_strategy(mock_report_api):
    expected_cost = 10
    mock_report_api(cost=expected_cost)
    strategy = ReportUsageStrategy(Message(text="report please", timestamp=datetime.datetime(2024, 1, 1, 0, 0, 0), id=42, report_id=3))
    assert strategy.calculate_usage() == expected_cost