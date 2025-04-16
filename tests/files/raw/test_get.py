from fastapi.testclient import TestClient
from src.finances_file_service.main import app

client = TestClient(app)


def test_get_csv_files():
    response = client.get("/api/v1/files/raw")
    assert response.status_code == 200
    assert response.json() == {"message": "Get CSV files endpoint"}
