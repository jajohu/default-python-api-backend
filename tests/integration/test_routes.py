import datetime
from http import HTTPStatus


def test_get_usage_route(test_client, mock_current_period_api):
    report_id = 42
    mock_current_period_api(report_id)
    response = test_client.get("/usage")
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert data.get("usage", False)
    for row in data["usage"]:
        assert type(row.get("message_id")) == int
        datetime.datetime.strptime(row.get("timestamp"), '%Y-%m-%dT%H:%M:%S.%fZ')
        assert row.get("report_name", False) is False or type(row.get("report_name")) == str
        assert type(row.get("credits_used")) == float
