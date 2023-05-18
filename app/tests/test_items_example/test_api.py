from app.main import app
from fastapi.testclient import TestClient

from app.config import settings

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_table_list():
    response = client.get(f"{settings.api_prefix}/example/table/list")
    assert response.status_code == 200
    content = response.json()
    assert content["success"] == True
    assert "data" in content
