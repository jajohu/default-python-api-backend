
from abc import ABC, abstractmethod

from app.models.message import Message


class UsageStrategy(ABC):
    def __init__(self, message: Message):
        self._message = message

    @abstractmethod
    def calculate_usage(self) -> float: ...