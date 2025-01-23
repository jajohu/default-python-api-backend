from app.usage_strategies.base import UsageStrategy


class TextMessageUsageStrategy(UsageStrategy):
    def calculate_usage(self) -> float:
        ...
