from pathlib import Path

from app.document_processing.document_loader import (
    DocumentLoader
)

from app.document_processing.txt_loader import (
    TXTLoader
)

from app.document_processing.pdf_loader import (
    PDFLoader
)

from app.document_processing.docx_loader import (
    DOCXLoader
)


class DocumentLoaderFactory:
    """
    Factory responsible for selecting
    the correct document loader.
    """


    _loaders = {

        ".txt":
            TXTLoader,

        ".pdf":
            PDFLoader,

        ".docx":
            DOCXLoader,

    }


    @classmethod
    def get_loader(
        cls,
        file_path: str | Path
    ) -> DocumentLoader:
        """
        Return the appropriate loader
        based on file extension.
        """

        path = Path(
            file_path
        )


        extension = (
            path.suffix.lower()
        )


        loader_class = (
            cls._loaders.get(
                extension
            )
        )


        if loader_class is None:

            raise ValueError(

                f"Unsupported document format: "
                f"{extension}"

            )


        return loader_class()