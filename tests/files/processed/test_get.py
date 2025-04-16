from fastapi.testclient import TestClient
from src.finances_file_service.main import app

client = TestClient(app)


def test_get_processed_files():
    response = client.get("/api/v1/files/processed")
    assert response.status_code == 200
    assert response.json() == {"message": "Get processed files endpoint"}
