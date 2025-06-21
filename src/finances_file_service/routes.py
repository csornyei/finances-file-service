from fastapi import APIRouter, Depends, HTTPException, UploadFile
from pydantic import BaseModel

import finances_file_service.controllers.process as process_controller
from finances_file_service.controllers.upload import UploadController
from finances_file_service.files import FileHandler, get_file_handler
from finances_file_service.logger import logger
from finances_file_service.producer import producer

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


class ProcessDataRequest(BaseModel):
    """
    Request model for processing data.
    """

    file_name: str
    delimiter: str = ";"


@router.post("/process")
async def process_data(
    body: ProcessDataRequest,
    handler: FileHandler = Depends(get_file_handler),
):
    """
    Endpoint to process data.
    """

    if not body.file_name:
        logger.error("File name is required")
        raise HTTPException(status_code=400, detail="File name is required")
    if not body.delimiter:
        logger.error("Delimiter is required")
        raise HTTPException(status_code=400, detail="Delimiter is required")

    try:
        full_file_path = handler.get_file_path(f"csv/{body.file_name}")

    except FileNotFoundError:
        logger.error(f"File {body.file_name} not found")
        raise HTTPException(status_code=404, detail="File not found")

    if not full_file_path:
        logger.error(f"File {body.file_name} not found")
        raise HTTPException(status_code=404, detail="File not found")

    processed_df = process_controller.process_file(
        full_file_path, delimiter=body.delimiter
    )

    if not processed_df.empty:
        # send each row as json to the RabbitMQ queue
        for _, row in processed_df.iterrows():
            message = row.to_dict()

            await producer.send_message(message, logger)

    return processed_df.to_dict(orient="records")


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

    try:
        files = handler.list_files("csv")

        csv_files = [{"file_name": file, "file_type": "csv"} for file in files]

        return {"files": [*csv_files]}
    except FileNotFoundError:
        logger.error("Directory not found")
        raise HTTPException(status_code=404, detail="Directory not found")
    except ValueError:
        logger.error("Invalid directory")
        raise HTTPException(status_code=400, detail="Invalid directory")
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        raise HTTPException(status_code=500, detail="Error listing files")
