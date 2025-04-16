import os
import pytest
import shutil


@pytest.fixture(scope="session", autouse=True)
def set_env_variables():
    """
    Set environment variables for all tests.
    This fixture is automatically applied to all tests.
    """

    print("Setting environment variables for testing...")
    os.environ["UPLOAD_DIRECTORY"] = "/tmp/uploads"
    os.environ["PROCESSED_DIRECTORY"] = "/tmp/processed"
    os.environ["LOG_LEVEL"] = "DEBUG"


@pytest.fixture(scope="function", autouse=True)
def clean_upload_directory():
    """
    Clean the /tmp/uploads directory after all tests have run.
    """
    upload_directory = "/tmp/uploads"

    # Ensure the directory exists before tests
    os.makedirs(upload_directory, exist_ok=True)

    # Yield control to the tests
    yield

    # Cleanup logic after all tests
    if os.path.exists(upload_directory):
        shutil.rmtree(upload_directory)
