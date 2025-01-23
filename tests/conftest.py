import pytest
import responses


@pytest.fixture
def mock_report_api():
    def setup_response(cost: float):
        with responses.RequestsMock() as response:
            response.add(
                responses.GET,
                "https://owpublic.blob.core.windows.net/tech-task/reports/42",
                json={"id": 42, "name": "test report name", "credit_cost": cost}
            )
            yield response
    return setup_response
