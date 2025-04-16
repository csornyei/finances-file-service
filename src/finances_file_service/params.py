import os
from pathlib import Path

from finances_file_service.logger import add_log_context, logger


def get_file_handler() -> str:
    """
    Get the file handler type from environment variables.
    """
    handler_type = os.getenv("FILE_HANDLER_TYPE", "local").lower()

    if handler_type not in ["local", "s3"]:
        logger.error(f"Unsupported file handler type: {handler_type}")
        raise ValueError(f"Unsupported file handler type: {handler_type}")

    add_log_context(file_handler_type=handler_type)

    return handler_type


def get_local_file_path() -> Path:
    """
    Get the local file path from environment variables.
    """
    local_file_path = os.getenv("LOCAL_FILE_PATH", "/tmp/uploads")
    os.makedirs(local_file_path, exist_ok=True)

    add_log_context(local_file_path=local_file_path)

    return Path(local_file_path)
