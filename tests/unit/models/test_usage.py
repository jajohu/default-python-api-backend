import datetime
from app.models.message import Message
from app.models.usage import Calculator, MessageUsage, Usage


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


# def test_calculator(mock_report_api):
#     expected_cost = 10
#     report_id = 42
#     report_name = "test report"
#     mock_report_api(cost=expected_cost, report_id=report_id, report_name=report_name)
#     messages = [Message(
#         id=1,
#         text="hi",
#         timestamp=datetime.datetime(2024, 1, 1)
#     ), Message(text="report please", timestamp=datetime.datetime(2024, 1, 1, 0, 0, 0), id=3, report_id=report_id)]
#     calculator = Calculator(messages)
#     usage = calculator.calculate_usage()
#     assert usage