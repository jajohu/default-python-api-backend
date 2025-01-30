from fastapi.testclient import TestClient
import pytest
from app.main import app


@pytest.fixture
def test_client():
    return TestClient(app)
