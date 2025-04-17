import os
import shutil

import pytest


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
