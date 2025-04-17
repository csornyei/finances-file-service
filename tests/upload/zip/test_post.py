import zipfile
from tempfile import TemporaryDirectory

from fastapi.testclient import TestClient

from finances_file_service.main import app

client = TestClient(app)


def test_upload_zip_no_file():
    # Test without a zip file
    response = client.post("/api/v1/upload/zip")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "zip_file"],
                "msg": "Field required",
                "input": None,
            }
        ]
    }


def test_upload_zip_invalid_file():
    # Test with an invalid file type
    files = {"zip_file": ("test.txt", "test", "text/plain")}
    response = client.post("/api/v1/upload/zip", files=files)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid file type. Only zip files are allowed."
    }


def test_upload_zip_empty_file():
    # Test with an empty zip file
    with TemporaryDirectory() as tmpdirname:
        zip_filename = f"{tmpdirname}/empty.zip"
        with zipfile.ZipFile(zip_filename, "w") as _:
            pass  # Create an empty zip file

        with open(zip_filename, "rb") as file:
            files = {"zip_file": ("empty.zip", file, "application/zip")}
            response = client.post("/api/v1/upload/zip", files=files)
        assert response.status_code == 200
        assert response.json() == {"message": "Upload zip data endpoint"}


def test_upload_zip():
    # Create a sample zip file
    with TemporaryDirectory() as tmpdirname:
        zip_filename = f"{tmpdirname}/test.zip"
        csv_content = "column1,column2,column3\nvalue1,value2,value3\n"

        with zipfile.ZipFile(zip_filename, "w") as zipf:
            zipf.writestr("test.csv", csv_content)
        with open(zip_filename, "rb") as file:
            files = {"zip_file": (zip_filename, file, "application/zip")}

            response = client.post("/api/v1/upload/zip", files=files)
        assert response.status_code == 200
        assert response.json() == {"message": "Upload zip data endpoint"}

        # Check if the file was saved correctly
        with open("/tmp/uploads/csv/test.csv", "rb") as file:
            content = file.read()
            assert content == csv_content.encode("utf-8")


def test_upload_zip_multiple_file():
    # Create a sample zip file with multiple CSV files
    with TemporaryDirectory() as tmpdirname:
        zip_filename = f"{tmpdirname}/test_multiple.zip"
        csv_content_1 = "column1,column2,column3\nvalue1,value2,value3\n"
        csv_content_2 = "columnA,columnB,columnC\nvalueA,valueB,valueC\n"

        with zipfile.ZipFile(zip_filename, "w") as zipf:
            zipf.writestr("test1.csv", csv_content_1)
            zipf.writestr("test2.csv", csv_content_2)

        with open(zip_filename, "rb") as file:
            files = {"zip_file": (zip_filename, file, "application/zip")}

            response = client.post("/api/v1/upload/zip", files=files)
        assert response.status_code == 200
        assert response.json() == {"message": "Upload zip data endpoint"}

        # Check if the files were saved correctly
        with open("/tmp/uploads/csv/test1.csv", "rb") as file:
            content = file.read()
            assert content == csv_content_1.encode("utf-8")

        with open("/tmp/uploads/csv/test2.csv", "rb") as file:
            content = file.read()
            assert content == csv_content_2.encode("utf-8")
