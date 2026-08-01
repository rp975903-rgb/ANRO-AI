from pathlib import Path

from docx import Document as DocxDocument

from app.document_processing.document_loader import (
    DocumentLoader
)


class DOCXLoader(DocumentLoader):
    """
    Loader for Microsoft Word DOCX documents.
    """


    def load(
        self,
        file_path: str | Path
    ) -> str:
        """
        Extract text from a DOCX file.
        """

        path = self.validate_file(
            file_path
        )


        if path.suffix.lower() != ".docx":

            raise ValueError(

                "DOCXLoader only supports .docx files."

            )


        document = DocxDocument(
            str(path)
        )


        paragraphs = []


        for paragraph in document.paragraphs:

            text = (
                paragraph.text.strip()
            )


            if text:

                paragraphs.append(
                    text
                )


        return "\n".join(
            paragraphs
        )