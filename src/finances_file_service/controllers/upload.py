import os
import zipfile
from tempfile import TemporaryDirectory

from finances_file_service.files.handlers import get_file_handler
from finances_file_service.logger import logger


class UploadController:
    def __init__(self):
        self.file_handler = get_file_handler()

    def upload_csv_file(self, file_path: str, content: bytes) -> None:
        """
        Upload a file to the specified path.

        :param file_path: The path where the file should be uploaded.
        :param content: The content of the file as bytes.
        """
        self.file_handler.save_file(f"csv/{file_path}", content)

    def upload_zip_file(self, prefix: str, file_path: str, content: bytes) -> None:
        """
        Upload a file to the specified path.

        :param file_path: The path where the file should be uploaded.
        :param content: The content of the file as bytes.
        """

        with TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, file_path)

            with open(file_path, "wb") as file:
                file.write(content)

            logger.info(f"File {file_path} uploaded successfully.")

            # Unzip the file
            logger.info(f"Unzipping file {file_path} to {temp_dir}")
            self._unzip_file(zip_file_path=file_path, extract_to=temp_dir)

            # List all files in the temporary directory
            files = os.listdir(temp_dir)

            # Upload each file to the specified path
            for file_name in files:
                logger.info(f"Processing file {file_name}")
                if file_name.endswith(".csv"):
                    with open(os.path.join(temp_dir, file_name), "rb") as file:
                        content = file.read()

                        self.upload_csv_file(f"{prefix}/{file_name}", content)

    def _unzip_file(self, zip_file_path: str, extract_to: str) -> None:
        """
        Unzips a ZIP file to the specified directory.

        :param zip_file_path: The path to the ZIP file.
        :param extract_to: The directory where the contents should be extracted.
        """
        try:
            # Check if the file exists
            if not os.path.exists(zip_file_path):
                logger.error(f"File {zip_file_path} does not exist.")
                raise FileNotFoundError(f"File {zip_file_path} does not exist.")

            # Open the ZIP file
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                # Extract all contents
                zip_ref.extractall(extract_to)
        except Exception as e:
            logger.error(f"Error unzipping file {zip_file_path}, error: {e}")
            raise e
