from pathlib import Path

from pypdf import PdfReader

from app.document_processing.document_loader import (
    DocumentLoader
)


class PDFLoader(DocumentLoader):
    """
    Loader for PDF documents.
    """


    def load(
        self,
        file_path: str | Path
    ) -> str:
        """
        Extract text from a PDF file.
        """

        path = self.validate_file(
            file_path
        )


        if path.suffix.lower() != ".pdf":

            raise ValueError(

                "PDFLoader only supports .pdf files."

            )


        reader = PdfReader(
            str(path)
        )


        pages_text = []


        for page in reader.pages:

            page_text = (
                page.extract_text()
            )


            if page_text:

                pages_text.append(
                    page_text
                )


        return "\n".join(
            pages_text
        )