import datetime

from app.message import Message, MessageType, Messages


def test_text_only_message():
    message = Message(text="test text", timestamp=datetime.datetime(2024, 1, 1, 0, 0, 0), id=42)
    assert message.type_ == MessageType.TEXT_ONLY


def test_report_message():
    message = Message(text="report please", timestamp=datetime.datetime(2024, 1, 1, 0, 0, 0), id=42, report_id=3)
    assert message.type_ == MessageType.REPORT


def test_messages():
    messages = Messages(messages=[Message(text="test text", timestamp=datetime.datetime(2024, 1, 1, 0, 0, 0), id=42), Message(text="report please", timestamp=datetime.datetime(2024, 1, 1, 0, 0, 0), id=43, report_id=3)])
    assert len(messages.messages) == 2