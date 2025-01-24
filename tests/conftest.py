from http import HTTPStatus
from fastapi.testclient import TestClient
import pytest
import responses
from app.main import app


@pytest.fixture
def mock_report_api():
    with responses.RequestsMock() as rsps:
        def setup_response(cost: float, report_id: int, report_name: str = "test report name", status_code: HTTPStatus = HTTPStatus.OK):
            rsps.add(
                responses.GET,
                f"https://owpublic.blob.core.windows.net/tech-task/reports/{report_id}",
                status=status_code,
                json={"id": report_id, "name": report_name, "credit_cost": cost}
            )
        yield setup_response


@pytest.fixture
def mock_current_period_api():
    with responses.RequestsMock() as rsps:
        def setup_response(report_id: int):
            rsps.add(
                responses.GET,
                "https://owpublic.blob.core.windows.net/tech-task/messages/current-period",
                json={"messages": [{"text": "test text message",
      "timestamp": "2024-04-29T03:25:03.613Z",
      "id": 1}, {"text": "please generate a report",
      "timestamp": "2024-04-29T02:08:29.375Z",
      "report_id": report_id,
      "id": 42}]}
            )
            rsps.add(
                responses.GET,
                f"https://owpublic.blob.core.windows.net/tech-task/reports/{report_id}",
                json={"id": report_id, "name": "test report name", "credit_cost": 1}
            )
        yield setup_response


@pytest.fixture
def test_client():
    return TestClient(app)
