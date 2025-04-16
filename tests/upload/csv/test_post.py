from fastapi.testclient import TestClient
from src.finances_file_service.main import app

client = TestClient(app)


def test_upload_csv():
    response = client.post("/api/v1/upload/csv")
    assert response.status_code == 200
    assert response.json() == {"message": "Upload CSV data endpoint"}
