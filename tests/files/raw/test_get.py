from fastapi.testclient import TestClient

from finances_file_service.main import app

client = TestClient(app)


def test_get_csv_files():
    with open("/tmp/uploads/csv/test.csv", "w") as file:
        file.write("column1,column2,column3\nvalue1,value2,value3\n")

    response = client.get("/api/v1/files/raw")
    assert response.status_code == 200
    assert response.json() == {
        "files": [
            {
                "file_name": "test.csv",
                "file_type": "csv",
            }
        ]
    }
