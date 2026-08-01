from app.database.database_manager import (
    DatabaseManager
)


class DocumentRepository:
    """
    Repository for document database operations.
    """


    def __init__(
        self,
        database_manager: DatabaseManager
    ):

        self.database = (
            database_manager
        )


    def create_document(
        self,
        document_id: str,
        filename: str,
        file_type: str,
        file_path: str,
        total_chunks: int = 0,
        status: str = "processed"
    ):

        query = """
            INSERT INTO documents (

                document_id,

                filename,

                file_type,

                file_path,

                total_chunks,

                status

            )

            VALUES (?, ?, ?, ?, ?, ?)
        """


        return self.database.execute(

            query,

            (

                document_id,

                filename,

                file_type,

                file_path,

                total_chunks,

                status

            )

        )


    def get_document(
        self,
        document_id: str
    ):

        query = """
            SELECT *

            FROM documents

            WHERE document_id = ?
        """


        return self.database.fetch_one(

            query,

            (
                document_id,
            )

        )


    def get_all_documents(self):

        query = """
            SELECT *

            FROM documents

            ORDER BY created_at DESC
        """


        return self.database.fetch_all(
            query
        )


    def delete_document(
        self,
        document_id: str
    ):

        query = """
            DELETE FROM documents

            WHERE document_id = ?
        """


        return self.database.execute(

            query,

            (
                document_id,
            )

        )