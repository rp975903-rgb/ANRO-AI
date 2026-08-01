from abc import ABC, abstractmethod
from pathlib import Path


class DocumentLoader(ABC):
    """
    Abstract base class for document loaders.

    Every document loader must implement
    the load() method.
    """


    def validate_file(
        self,
        file_path: str | Path
    ) -> Path:
        """
        Validate that the file exists
        and is actually a file.
        """

        path = Path(
            file_path
        )


        if not path.exists():

            raise FileNotFoundError(

                f"Document not found: {path}"

            )


        if not path.is_file():

            raise ValueError(

                f"Path is not a file: {path}"

            )


        return path


    @abstractmethod
    def load(
        self,
        file_path: str | Path
    ) -> str:
        """
        Load document and return extracted text.
        """

        raise NotImplementedError