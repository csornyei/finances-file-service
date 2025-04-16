import os
from pathlib import Path

from finances_file_service.files.local_handler import LocalHandler
from finances_file_service.files.s3_handler import S3Handler
from finances_file_service.files.file_handler import FileHandler


def get_file_handler() -> FileHandler:
    handler_type = os.getenv("FILE_HANDLER_TYPE", "local").lower()

    if handler_type == "local":
        base_path = Path(os.getenv("LOCAL_FILE_PATH", "/tmp"))
        return LocalHandler(base_path)
    elif handler_type == "s3":
        return S3Handler()
    else:
        raise ValueError(f"Unsupported file handler type: {handler_type}")
