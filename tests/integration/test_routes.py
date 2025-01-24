from http import HTTPStatus


def test_get_usage_route(test_client, mock_current_period_api):
    report_id = 42
    mock_current_period_api(report_id)
    response = test_client.get("/usage")
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert data.get("usage", False)
    for row in data["usage"]:
        assert type(row.get("message_id", False)) == int
        assert type(row.get("timestamp", False)) == str
        assert row.get("report_name", False) is None or type(row.get("report_name", False)) == str
        assert type(row.get("credits_used", False)) == float
