from fastapi import APIRouter

router = APIRouter()


@router.post("/upload/zip")
async def upload_zip():
    """
    Endpoint to upload zip data.
    """
    return {"message": "Upload zip data endpoint"}


@router.post("/upload/csv")
async def upload_csv():
    """
    Endpoint to upload CSV data.
    """
    return {"message": "Upload CSV data endpoint"}


@router.post("/process")
async def process_data():
    """
    Endpoint to process data.
    """
    return {"message": "Process data endpoint"}


@router.get("/files/raw")
async def get_csv_files():
    """
    Endpoint to get CSV files.
    """
    return {"message": "Get CSV files endpoint"}


@router.get("/files/processed")
async def get_processed_files():
    """
    Endpoint to get processed files.
    """
    return {"message": "Get processed files endpoint"}
