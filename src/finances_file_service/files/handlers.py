from finances_file_service import params
from finances_file_service.files.file_handler import FileHandler
from finances_file_service.files.local_handler import LocalHandler
from finances_file_service.files.s3_handler import S3Handler


def get_file_handler() -> FileHandler:
    handler_type = params.get_file_handler()

    if handler_type == "local":
        base_path = params.get_local_file_path()
        return LocalHandler(base_path)
    elif handler_type == "s3":
        return S3Handler()
    else:
        raise ValueError(f"Unsupported file handler type: {handler_type}")
