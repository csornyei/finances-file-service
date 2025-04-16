from fastapi.testclient import TestClient

from finances_file_service.main import app

client = TestClient(app)


def test_process_data():
    # write file to csv dir
    columns = [
        "Date",
        "Interest Date",
        "Description",
        "Counterparty",
        "Name",
        "Account",
        "Amount",
    ]

    data = [
        {
            "Date": "2025-01-01",
            "Interest Date": "2025-01-01",
            "Description": "Test description",
            "Counterparty": "Test counterparty",
            "Name": "Test name",
            "Account": "Test account",
            "Amount": "1.000,00",
        }
    ]

    csv_content = ";".join(columns)
    for row in data:
        csv_content += "\n" + ";".join(str(row[col]) for col in columns)

    with open("/tmp/uploads/csv/test.csv", "w") as file:
        file.write(csv_content)

    body = {
        "file_name": "test.csv",
        "delimiter": ";",
    }

    response = client.post("/api/v1/process", json=body)
    assert response.status_code == 200

    assert response.json() == [
        {
            "date": "2025-01-01T00:00:00",
            "interest_date": "2025-01-01T00:00:00",
            "description": "Test description",
            "counterparty_iban": "Test counterparty",
            "counterparty_name": "Test name",
            "account": "Test account",
            "amount": 100000,
        }
    ]
