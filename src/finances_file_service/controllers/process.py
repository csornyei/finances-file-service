import pandas as pd


def process_file(file_path: str, delimiter: str = ";") -> pd.DataFrame:
    df = pd.read_csv(file_path, delimiter=delimiter)

    df = df.rename(
        columns={
            "Date": "date",
            "Interest Date": "interest_date",
            "Description": "description",
            "Counterparty": "counterparty_iban",
            "Name": "counterparty_name",
            "Account": "account",
            "Amount": "amount",
        }
    )

    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    df["interest_date"] = pd.to_datetime(
        df["interest_date"], format="%Y-%m-%d", errors="coerce"
    )
    df["description"] = df["description"].str.replace("&amp;", "&").fillna("")
    df["counterparty_name"] = df["counterparty_name"].str.replace("&amp;", "&")

    df["counterparty_iban"] = df["counterparty_iban"].fillna("")

    df["amount"] = pd.to_numeric(
        df["amount"].str.replace(".", "").str.replace(",", ".")
    )
    df["amount"] = (df["amount"] * 100).astype(int)

    return df
