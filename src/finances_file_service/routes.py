from fastapi import APIRouter, Depends, HTTPException, UploadFile

from finances_file_service.controllers.upload import UploadController
from finances_file_service.files import FileHandler, get_file_handler
from finances_file_service.logger import logger

router = APIRouter()


@router.post("/upload/zip")
async def upload_zip(
    zip_file: UploadFile, controller: UploadController = Depends(UploadController)
):
    """
    Endpoint to upload zip data.
    """

    if not zip_file or zip_file.content_type != "application/zip":
        logger.error(
            f"Invalid file type: {zip_file.content_type}. Only zip files are allowed."
        )
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only zip files are allowed."
        )

    file_name = zip_file.filename

    if not file_name.endswith(".zip"):
        logger.error("File is not a zip file")
        raise HTTPException(status_code=400, detail="File is not a zip file")

    file_content = await zip_file.read()

    try:
        controller.upload_zip_file(file_name, file_content)

        return {"message": "Upload zip data endpoint"}
    except Exception as e:
        logger.error(f"Error uploading zip file: {e}")
        raise HTTPException(status_code=500, detail="Error processing zip file")


@router.post("/upload/csv")
async def upload_csv(
    csv_file: UploadFile, controller: UploadController = Depends(UploadController)
):
    """
    Endpoint to upload CSV data.
    """

    if not csv_file or csv_file.content_type != "text/csv":
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only CSV files are allowed."
        )

    file_name = csv_file.filename

    if not file_name.endswith(".csv"):
        return {"error": "File is not a CSV file"}

    file_content = await csv_file.read()

    controller.upload_csv_file(file_name, file_content)

    return {"message": "Upload CSV data endpoint"}


@router.post("/process")
async def process_data():
    """
    Endpoint to process data.
    """
    return {"message": "Process data endpoint"}


@router.get("/files/raw")
async def get_csv_files(
    handler: FileHandler = Depends(get_file_handler),
):
    """
    Endpoint to get CSV files.
    """

    if not handler:
        logger.error("File handler not found")
        raise HTTPException(status_code=404, detail="File handler not found")

    csv_files = [
        {"file_name": file, "file_type": "csv"} for file in handler.list_files("csv")
    ]

    return {"files": [*csv_files]}
