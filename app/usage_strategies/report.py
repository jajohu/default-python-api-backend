from http import HTTPStatus
import requests
from app.exceptions import ReportNotFound
from app.models.message import Message
from app.models.report import Report
from app.usage_strategies.base import UsageResult, UsageStrategy


class ReportUsageStrategy(UsageStrategy):
    BASE_COST = 0

    def calculate_usage(self, message: Message) -> UsageResult:
        self._reset_current_usage()
        report_response = requests.get(self.get_endpoint_url(message.report_id), timeout=30)
        if report_response.status_code == HTTPStatus.NOT_FOUND:
            raise ReportNotFound(f"Could not find report ID {message.report_id}")
        report = Report.model_validate(report_response.json())
        self._current_usage = report.credit_cost
        return UsageResult(usage=self._current_usage, report_name=report.name)

    def get_endpoint_url(self, report_id: int) -> str:
        return f"https://owpublic.blob.core.windows.net/tech-task/reports/{report_id}"
