import requests
from app.models.message import Message
from app.models.report import Report
from app.usage_strategies.base import UsageStrategy


class ReportUsageStrategy(UsageStrategy):
    BASE_COST = 0

    def calculate_usage(self, message: Message) -> float:
        self._reset_current_usage()
        report_response = requests.get(self.get_endpoint_url(message.report_id)).json()
        report = Report.model_validate(report_response)
        self._current_usage = report.credit_cost
        return self._current_usage

    def get_endpoint_url(self, report_id: int) -> str:
        return f"https://owpublic.blob.core.windows.net/tech-task/reports/{report_id}"