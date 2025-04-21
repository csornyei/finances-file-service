import os
import shutil
from unittest.mock import AsyncMock, MagicMock

from finances_file_service.producer import RabbitMQProducer, get_producer
from finances_file_service.main import app

import pytest


@pytest.fixture
def mock_producer():
    mock = MagicMock(spec=RabbitMQProducer)
    mock.connect = AsyncMock(return_value=mock)
    mock.send_message = AsyncMock()
    return mock


@pytest.fixture
def override_dependency(mock_producer):
    async def _override():
        yield mock_producer

    app.dependency_overrides[get_producer] = _override
    yield
    app.dependency_overrides.clear()


@pytest.fixture(scope="session", autouse=True)
def set_env_variables():
    """
    Set environment variables for all tests.
    This fixture is automatically applied to all tests.
    """

    print("Setting up environment variables for tests...")
    os.environ["FILE_HANDLER_TYPE"] = "local"
    os.environ["LOCAL_FILE_PATH"] = "/tmp/uploads"
    os.environ["LOG_LEVEL"] = "DEBUG"


@pytest.fixture(scope="function", autouse=True)
def clean_upload_directory():
    """
    Clean the /tmp/uploads directory after all tests have run.
    """
    upload_directory = os.getenv("LOCAL_FILE_PATH", "/tmp/uploads")

    os.makedirs(upload_directory, exist_ok=True)
    os.makedirs(os.path.join(upload_directory, "csv"), exist_ok=True)

    # Ensure the directory exists before tests
    os.makedirs(upload_directory, exist_ok=True)

    # Yield control to the tests
    yield

    # Cleanup logic after all tests
    if os.path.exists(upload_directory):
        shutil.rmtree(upload_directory)
