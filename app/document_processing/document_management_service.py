from pathlib import Path

from app.database.metadata_database import MetadataDatabase

from app.document_processing.document_processor import DocumentProcessor


class DocumentManagementService:
    """
    High-level document management service.

    Responsibilities:

    - Add documents
    - List documents
    - Search documents
    - Get statistics
    - Delete documents
    - Re-index documents
    """

    def __init__(self):

        self.processor = DocumentProcessor()

        self.database = MetadataDatabase()


    # ========================================================
    # ADD DOCUMENT
    # ========================================================

    def add_document(
        self,
        file_path: str | Path
    ) -> dict:
        """
        Process and register a new document.
        """

        path = Path(file_path)

        if not path.exists():

            raise FileNotFoundError(

                f"Document not found: {path}"

            )

        result = self.processor.process(

            path

        )

        document = result["document"]

        return {

            "document": document,

            "total_chunks":
                result["total_chunks"],

            "storage_path":
                result["storage_path"],

        }


    # ========================================================
    # LIST DOCUMENTS
    # ========================================================

    def list_documents(self):

        return (

            self.database

            .get_all_documents()

        )


    # ========================================================
    # SEARCH DOCUMENTS
    # ========================================================

    def search_documents(
        self,
        keyword: str
    ):

        return (

            self.database

            .search_documents(

                keyword

            )

        )


    # ========================================================
    # GET STATISTICS
    # ========================================================

    def get_statistics(self):
        """
        Return document database statistics.
        """

        documents = (

            self.database

            .get_all_documents()

        )


        total_documents = len(

            documents

        )


        total_chunks = sum(

            document.get(

                "total_chunks",

                0

            )

            for document in documents

        )


        processed_documents = sum(

            1

            for document in documents

            if document.get(

                "status"

            ) == "processed"

        )


        failed_documents = sum(

            1

            for document in documents

            if document.get(

                "status"

            ) == "failed"

        )


        return {

            "total_documents":
                total_documents,

            "total_chunks":
                total_chunks,

            "processed_documents":
                processed_documents,

            "failed_documents":
                failed_documents,

        }


    # ========================================================
    # DELETE DOCUMENT
    # ========================================================

    def delete_document(

        self,

        document_id: str

    ) -> bool:
        """
        Delete processed document data
        and database metadata.
        """

        document = (

            self.database

            .get_document(

                document_id

            )

        )


        if not document:

            return False


        # ==========================================
        # DELETE PROCESSED JSON
        # ==========================================

        storage_path = document.get(

            "storage_path"

        )


        if storage_path:

            json_file = Path(

                storage_path

            )


            if json_file.exists():

                json_file.unlink()


        # ==========================================
        # DELETE DATABASE METADATA
        # ==========================================

        deleted = (

            self.database

            .delete_document(

                document_id

            )

        )


        return deleted


    # ========================================================
    # RE-INDEX DOCUMENT
    # ========================================================

    def reindex_document(

        self,

        file_path: str | Path

    ) -> dict:
        """
        Re-process an existing document.
        """

        return self.add_document(

            file_path

        )