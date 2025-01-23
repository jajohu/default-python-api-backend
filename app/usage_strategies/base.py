
from abc import ABC, abstractmethod

from app.models.message import Messages


class UsageStrategy(ABC):
    def __init__(self, messages: Messages):
        self._messages = messages

    @abstractmethod
    def calculate_usage(self) -> float: ...