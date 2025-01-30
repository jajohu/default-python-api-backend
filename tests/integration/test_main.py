from http import HTTPStatus


def test_health_check(test_client):
    response = test_client.get("/health")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["status"] == "ok"
