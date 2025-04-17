from fastapi.testclient import TestClient

from finances_file_service.main import app

client = TestClient(app)


def test_upload_csv():
    # Create a mock CSV file
    csv_content = "column1,column2,column3\nvalue1,value2,value3\n"
    files = {"csv_file": ("test.csv", csv_content, "text/csv")}

    # Send a POST request to the /upload/csv endpoint
    response = client.post("/api/v1/upload/csv", files=files)

    # Assert the response
    assert response.status_code == 200
    assert response.json() == {"message": "Upload CSV data endpoint"}

    # Uploaded file should be saved in the expected location
    with open("/tmp/uploads/csv/test.csv", "rb") as file:
        content = file.read()
        assert content == csv_content.encode("utf-8")
