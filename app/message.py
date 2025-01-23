import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, field_validator


class MessageType(str, Enum):
    TEXT_ONLY = "test_only"
    REPORT = "report"


class Message(BaseModel):
    text: str
    timestamp: datetime.datetime
    report_id: int | None = None
    id: int
    type_: MessageType = MessageType.TEXT_ONLY

    @field_validator("type_", mode="before")
    def validate_message_type(cls, _, info):
        return MessageType.REPORT if info.data.get("report_id") else MessageType.TEXT_ONLY