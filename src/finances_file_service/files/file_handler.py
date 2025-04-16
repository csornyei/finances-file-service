from abc import ABC, abstractmethod
from typing import List


class FileHandler(ABC):
    @abstractmethod
    def list_files(self, directory: str) -> List[str]:
        """
        List all files in the specified directory.

        :param directory: The directory to list files from.
        :return: A list of file names.
        """
        pass

    @abstractmethod
    def save_file(self, file_path: str, content: bytes) -> None:
        """
        Save a file to the specified path.

        :param file_path: The path where the file should be saved.
        :param content: The content of the file as bytes.
        """
        pass
