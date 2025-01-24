
from abc import ABC, abstractmethod

from app.models.message import Message


class UsageStrategy(ABC):
    BASE_COST: float = NotImplemented

    def __init__(self):
        self._current_usage = self.BASE_COST

    @abstractmethod
    def calculate_usage(self, message: Message) -> float: ...

    def _reset_current_usage(self):
        self._current_usage = self.BASE_COST