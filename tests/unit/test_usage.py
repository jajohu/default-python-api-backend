import datetime
from app.message import Message
from app.usage import MessageUsage, Usage


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