import requests
from app.models.message import Messages
from app.models.usage import Calculator, Usage
from app.usage_strategies.report import ReportUsageStrategy
from app.usage_strategies.text_message import TextMessageUsageStrategy

CURRENT_PERIOD_ENDPOINT = "https://owpublic.blob.core.windows.net/tech-task/messages/current-period"


def get_usage() -> Usage:
    messages = Messages.model_validate(requests.get(CURRENT_PERIOD_ENDPOINT, timeout=30).json())
    calculator = Calculator(messages, TextMessageUsageStrategy(), ReportUsageStrategy())
    return calculator.calculate_usage()
