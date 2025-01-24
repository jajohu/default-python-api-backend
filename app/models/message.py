import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, computed_field


class MessageType(str, Enum):
    TEXT_ONLY = "test_only"
    REPORT = "report"


class Message(BaseModel):
    text: str
    timestamp: datetime.datetime
    report_id: int | None = None
    id: int

    @computed_field
    def type_(self) -> MessageType:
        return MessageType.REPORT if self.report_id is not None else MessageType.TEXT_ONLY


class Messages(BaseModel):
    messages: List[Message]
