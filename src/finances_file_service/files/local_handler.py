from pathlib import Path
from typing import List
import os

from finances_file_service.files.file_handler import FileHandler


class LocalHandler(FileHandler):
    def __init__(self, base_path: Path):
        super().__init__()

        self.base_path = base_path

        if not self.base_path.is_dir():
            raise ValueError(f"Base path {self.base_path} is not a directory.")

    def list_files(self, directory: str) -> List[str]:
        """
        List all files in the specified directory.

        :param directory: The directory to list files from.
        :return: A list of file names.

        :raises ValueError: If the directory is not a valid directory.
        :raises FileNotFoundError: If the directory does not exist.
        """

        full_path = Path(self.base_path) / directory

        if not full_path.is_dir():
            raise ValueError(f"Path {full_path} is not a directory.")
        if not full_path.exists():
            raise FileNotFoundError(f"Directory {full_path} does not exist.")

        return [file.name for file in full_path.iterdir() if file.is_file()]

    def save_file(self, file_path: str, content: bytes) -> None:
        """
        Save a file to the specified path.

        :param file_path: The path where the file should be saved.
        :param content: The content of the file as bytes.

        :raises ValueError: If the directory is not a valid directory.
        """
        full_path = Path(self.base_path) / file_path

        if not full_path.parent.exists():
            print(f"Directory {full_path.parent} does not exist. Creating it.")
            os.mkdir(full_path.parent)
        if not full_path.parent.is_dir():
            raise ValueError(f"Path {full_path.parent} is not a directory.")

        with open(full_path, "wb") as file:
            file.write(content)
