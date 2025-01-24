from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.models.message import Message


@dataclass
class UsageResult:
    usage: float
    report_name: str | None


# pylint: disable=R0903
class UsageStrategy(ABC):
    BASE_COST: float = NotImplemented

    def __init__(self):
        self._current_usage = self.BASE_COST

    @abstractmethod
    def calculate_usage(self, message: Message) -> UsageResult: ...

    def _reset_current_usage(self):
        self._current_usage = self.BASE_COST
