import datetime
from typing import Generator, List
from pydantic import BaseModel, Field, field_serializer

from app.exceptions import ReportNotFound
from app.models.message import MessageType, Messages
from app.usage_strategies.base import UsageStrategy


class MessageUsage(BaseModel):
    message_id: int
    timestamp: datetime.datetime
    report_name: str | None = None
    credits_used: float

    @field_serializer('timestamp')
    def serialize_datetime(self, dt: datetime.datetime) -> str:
        return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'


class Usage(BaseModel):
    usage: List[MessageUsage]


class Calculator:
    def __init__(self, messages: Messages, text_message_strategy: UsageStrategy, report_strategy: UsageStrategy):
        self._messages = messages
        self._text_message_strategy = text_message_strategy
        self._report_strategy = report_strategy

    def calculate_usage(self) -> Usage:
        return Usage(usage=list(self._yield_from_messages()))
    
    def _yield_from_messages(self) -> Generator[MessageUsage, None, None]:
        for message in self._messages.messages:
            match message.type_:
                case MessageType.TEXT_ONLY:
                    usage = self._text_message_strategy.calculate_usage(message)
                    yield MessageUsage(message_id=message.id, timestamp=message.timestamp, credits_used=usage.usage)
                case MessageType.REPORT:
                    try:
                        usage = self._report_strategy.calculate_usage(message)
                        yield MessageUsage(message_id=message.id, timestamp=message.timestamp, report_name=usage.report_name, credits_used=usage.usage)
                    except ReportNotFound:
                        usage = self._text_message_strategy.calculate_usage(message)
                        yield MessageUsage(message_id=message.id, timestamp=message.timestamp, credits_used=usage.usage)
