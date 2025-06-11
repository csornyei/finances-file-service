import os
from pathlib import Path

from finances_file_service.logger import logger
from finances_shared import add_log_context


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


def get_rabbitmq_connection() -> str:
    """
    Get the RabbitMQ connection string from environment variables.
    - RABBITMQ_HOST=rabbitmq
    - RABBITMQ_PORT=5672
    - RABBITMQ_USER=guest
    - RABBITMQ_PASSWORD=guest
    """
    rabbitmq_host = os.getenv("RABBITMQ_HOST")
    rabbitmq_port = os.getenv("RABBITMQ_PORT")
    rabbitmq_user = os.getenv("RABBITMQ_USER")
    rabbitmq_password = os.getenv("RABBITMQ_PASSWORD")

    if (
        not rabbitmq_host
        or not rabbitmq_port
        or not rabbitmq_user
        or not rabbitmq_password
    ):
        logger.error(
            "RabbitMQ connection parameters are not set in environment variables."
        )
        raise ValueError(
            "RabbitMQ connection parameters are not set in environment variables."
        )

    return (
        f"amqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_host}:{rabbitmq_port}/"
    )
