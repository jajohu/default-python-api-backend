import datetime
from app.message import Message
from app.usage import MessageUsage


def test_message_usage():
    message_usage = MessageUsage(message_id=42, timestamp=datetime.datetime(2024, 1, 1, 0, 0, 0), credits_used=1)
    assert message_usage.message_id == 42
    assert message_usage.timestamp == datetime.datetime(2024, 1, 1, 0, 0, 0)
    assert message_usage.report_name is None
    assert message_usage.credits_used == 1


def test_report_usage():
    ...


def test_usage():
    ...