import zipfile
from fastapi.testclient import TestClient

from finances_file_service.main import app

client = TestClient(app)


def test_upload_zip():
    # Create a sample zip file

    zip_filename = "test.zip"
    csv_content = "column1,column2,column3\nvalue1,value2,value3\n"

    with zipfile.ZipFile(zip_filename, "w") as zipf:
        zipf.writestr("test.csv", csv_content)
    with open(zip_filename, "rb") as file:
        files = {"zip_file": (zip_filename, file, "application/zip")}

        response = client.post("/api/v1/upload/zip", files=files)
    assert response.status_code == 200
    assert response.json() == {"message": "Upload zip data endpoint"}

    # Check if the file was saved correctly
    with open("/tmp/csv/test.csv", "rb") as file:
        content = file.read()
        assert content == csv_content.encode("utf-8")
