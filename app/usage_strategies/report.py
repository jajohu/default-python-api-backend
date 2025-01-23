import requests
from app.models.report import Report
from app.usage_strategies.base import UsageStrategy


class ReportUsageStrategy(UsageStrategy):

    def calculate_usage(self) -> float:
        report_response = requests.get(self.endpoint_url).json()
        report = Report.model_validate(report_response)
        return report.credit_cost

    @property
    def endpoint_url(self) -> str:
        return f"https://owpublic.blob.core.windows.net/tech-task/reports/{self._message.report_id}"