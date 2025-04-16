from fastapi.testclient import TestClient
from src.finances_file_service.main import app

client = TestClient(app)


def test_process_data():
    response = client.post("/api/v1/process")
    assert response.status_code == 200
    assert response.json() == {"message": "Process data endpoint"}
