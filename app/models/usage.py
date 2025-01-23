import datetime
from typing import List
from pydantic import BaseModel


class MessageUsage(BaseModel):
    message_id: int
    timestamp: datetime.datetime
    report_name: str | None = None
    credits_used: float


class Usage(BaseModel):
    usage: List[MessageUsage]


class Calculator:
    ...
