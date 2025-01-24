import datetime
from app.models.message import Message, Messages
from app.models.usage import Calculator, MessageUsage, Usage
from app.usage_strategies.report import ReportUsageStrategy
from app.usage_strategies.text_message import TextMessageUsageStrategy


def test_message_usage():
    message_usage = MessageUsage(message_id=42, timestamp=datetime.datetime(2024, 1, 1, 0, 0, 0), credits_used=1)
    assert message_usage.message_id == 42
    assert message_usage.timestamp == datetime.datetime(2024, 1, 1, 0, 0, 0)
    assert message_usage.report_name is None
    assert message_usage.credits_used == 1


def test_report_usage():
    report_usage = MessageUsage(message_id=42, timestamp=datetime.datetime(2024, 1, 1, 0, 0, 0), report_name="test report name", credits_used=1)
    assert report_usage.message_id == 42
    assert report_usage.timestamp == datetime.datetime(2024, 1, 1, 0, 0, 0)
    assert report_usage.report_name == "test report name"
    assert report_usage.credits_used == 1


def test_usage():
    usage = Usage(usage=[MessageUsage(message_id=42, timestamp=datetime.datetime(2024, 1, 1, 0, 0, 0), report_name="test report name", credits_used=1), MessageUsage(message_id=43, timestamp=datetime.datetime(2024, 1, 1, 0, 0, 0), credits_used=1)])
    assert len(usage.usage) == 2


def test_calculator(mock_report_api):
    expected_cost = 10
    report_id = 42
    report_name = "test report"
    mock_report_api(cost=expected_cost, report_id=report_id, report_name=report_name)
    messages = [Message(
        id=1,
        text="hi",
        timestamp=datetime.datetime(2024, 1, 1)
    ), Message(text="report please", timestamp=datetime.datetime(2024, 1, 1, 0, 0, 0), id=3, report_id=report_id)]
    calculator = Calculator(Messages(messages=messages), TextMessageUsageStrategy(), ReportUsageStrategy())
    usage = calculator.calculate_usage()
    total_usage = sum(usage.credits_used for usage in usage.usage)
    assert total_usage == 11


def test_calculator_report_not_found_fallback(mock_report_api):
    report_id = 999
    mock_report_api(cost=0, report_id=report_id, status_code=404)
    messages = [Message(
        text="report please",
        timestamp=datetime.datetime(2024, 1, 1),
        id=1,
        report_id=report_id
    )]
    calculator = Calculator(
        Messages(messages=messages),
        TextMessageUsageStrategy(),
        ReportUsageStrategy()
    )
    usage = calculator.calculate_usage()
    message_usage = usage.usage[0]
    assert message_usage.credits_used == TextMessageUsageStrategy.BASE_COST