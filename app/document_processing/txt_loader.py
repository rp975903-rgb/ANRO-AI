from pathlib import Path

from app.document_processing.document_loader import (
    DocumentLoader
)


class TXTLoader(DocumentLoader):
    """
    Loader for plain text files.
    """


    def load(
        self,
        file_path: str | Path
    ) -> str:
        """
        Read a TXT file and return its content.
        """

        path = self.validate_file(
            file_path
        )


        if path.suffix.lower() != ".txt":

            raise ValueError(

                "TXTLoader only supports .txt files."

            )


        try:

            text = path.read_text(
                encoding="utf-8"
            )


        except UnicodeDecodeError:

            text = path.read_text(
                encoding="latin-1"
            )


        return text