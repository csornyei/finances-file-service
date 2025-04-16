from fastapi.testclient import TestClient
from src.finances_file_service.main import app

client = TestClient(app)


def test_upload_zip():
    response = client.post("/api/v1/upload/zip")
    assert response.status_code == 200
    assert response.json() == {"message": "Upload zip data endpoint"}
