from pathlib import Path

import sqlite3

from datetime import datetime


class MetadataDatabase:
    """
    SQLite database for storing document metadata.

    Stores:

    - Document ID
    - User ID
    - Filename
    - File type
    - Original file path
    - Processed storage path
    - Number of chunks
    - Processing status
    - Created time
    - Updated time
    """


    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(

        self,

        database_path: str | Path = (

            "data/metadata/documents.db"

        )

    ):

        self.database_path = Path(

            database_path

        )


        # ====================================================
        # CREATE PARENT DIRECTORY
        # ====================================================

        self.database_path.parent.mkdir(

            parents=True,

            exist_ok=True

        )


        # ====================================================
        # INITIALIZE DATABASE
        # ====================================================

        self.create_table()


        # ====================================================
        # ENSURE USER ID COLUMN EXISTS
        # ====================================================

        self.ensure_user_id_column()


    # ========================================================
    # DATABASE CONNECTION
    # ========================================================

    def get_connection(

        self

    ):

        connection = sqlite3.connect(

            str(

                self.database_path

            )

        )


        connection.row_factory = (

            sqlite3.Row

        )


        return connection


    # ========================================================
    # CREATE TABLE
    # ========================================================

    def create_table(

        self

    ):

        sql_query = """

        CREATE TABLE IF NOT EXISTS documents (

            document_id TEXT PRIMARY KEY,

            user_id INTEGER,

            filename TEXT NOT NULL,

            file_type TEXT NOT NULL,

            file_path TEXT NOT NULL,

            storage_path TEXT,

            total_chunks INTEGER DEFAULT 0,

            status TEXT DEFAULT 'processed',

            created_at TEXT NOT NULL,

            updated_at TEXT NOT NULL

        )

        """


        with self.get_connection() as connection:

            connection.execute(

                sql_query

            )


            connection.commit()


    # ========================================================
    # ENSURE USER ID COLUMN EXISTS
    # ========================================================

    def ensure_user_id_column(

        self

    ):

        """
        Add user_id column to existing databases.

        This prevents errors when an old
        documents.db already exists.
        """

        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                PRAGMA table_info(documents)

                """

            )


            columns = [

                row["name"]

                for row in cursor.fetchall()

            ]


            if "user_id" not in columns:

                connection.execute(

                    """

                    ALTER TABLE documents

                    ADD COLUMN user_id INTEGER

                    """

                )


                connection.commit()


    # ========================================================
    # ADD DOCUMENT
    # ========================================================

    def add_document(

        self,

        document_id: str,

        filename: str,

        file_type: str,

        file_path: str,

        storage_path: str,

        total_chunks: int,

        status: str = "processed",

        user_id: int | None = None

    ):

        """
        Add document metadata.

        The document is associated with
        the authenticated user's ID.
        """

        now = datetime.now().isoformat(

            timespec="seconds"

        )


        with self.get_connection() as connection:

            connection.execute(

                """

                INSERT OR REPLACE INTO documents (

                    document_id,

                    user_id,

                    filename,

                    file_type,

                    file_path,

                    storage_path,

                    total_chunks,

                    status,

                    created_at,

                    updated_at

                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

                """,

                (

                    document_id,

                    user_id,

                    filename,

                    file_type,

                    file_path,

                    storage_path,

                    total_chunks,

                    status,

                    now,

                    now

                )

            )


            connection.commit()


        return True


    # ========================================================
    # GET ONE DOCUMENT
    # ========================================================

    def get_document(

        self,

        document_id: str

    ):

        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                SELECT *

                FROM documents

                WHERE document_id = ?

                """,

                (

                    document_id,

                )

            )


            row = cursor.fetchone()


        if row:

            return dict(

                row

            )


        return None


    # ========================================================
    # GET DOCUMENT FOR USER
    # ========================================================

    def get_user_document(

        self,

        document_id: str,

        user_id: int

    ):

        """
        Get a document only if it belongs
        to the authenticated user.
        """

        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                SELECT *

                FROM documents

                WHERE

                    document_id = ?

                    AND user_id = ?

                """,

                (

                    document_id,

                    user_id

                )

            )


            row = cursor.fetchone()


        if row:

            return dict(

                row

            )


        return None


    # ========================================================
    # GET ALL DOCUMENTS
    # ========================================================

    def get_all_documents(

        self

    ):

        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                SELECT *

                FROM documents

                ORDER BY created_at DESC

                """

            )


            rows = cursor.fetchall()


        return [

            dict(

                row

            )

            for row in rows

        ]


    # ========================================================
    # GET ALL DOCUMENTS FOR USER
    # ========================================================

    def get_user_documents(

        self,

        user_id: int

    ):

        """
        Return only documents belonging
        to the authenticated user.
        """

        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                SELECT *

                FROM documents

                WHERE user_id = ?

                ORDER BY created_at DESC

                """,

                (

                    user_id,

                )

            )


            rows = cursor.fetchall()


        return [

            dict(

                row

            )

            for row in rows

        ]


    # ========================================================
    # CHECK DOCUMENT EXISTS
    # ========================================================

    def document_exists(

        self,

        document_id: str

    ) -> bool:

        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                SELECT 1

                FROM documents

                WHERE document_id = ?

                LIMIT 1

                """,

                (

                    document_id,

                )

            )


            result = cursor.fetchone()


        return result is not None


    # ========================================================
    # CHECK USER DOCUMENT EXISTS
    # ========================================================

    def user_document_exists(

        self,

        document_id: str,

        user_id: int

    ) -> bool:

        """
        Check whether a document belongs
        to the authenticated user.
        """

        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                SELECT 1

                FROM documents

                WHERE

                    document_id = ?

                    AND user_id = ?

                LIMIT 1

                """,

                (

                    document_id,

                    user_id

                )

            )


            result = cursor.fetchone()


        return result is not None


    # ========================================================
    # UPDATE DOCUMENT STATUS
    # ========================================================

    def update_status(

        self,

        document_id: str,

        status: str

    ):

        now = datetime.now().isoformat(

            timespec="seconds"

        )


        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                UPDATE documents

                SET

                    status = ?,

                    updated_at = ?

                WHERE document_id = ?

                """,

                (

                    status,

                    now,

                    document_id

                )

            )


            connection.commit()


            return cursor.rowcount > 0


    # ========================================================
    # DELETE DOCUMENT
    # ========================================================

    def delete_document(

        self,

        document_id: str

    ):

        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                DELETE FROM documents

                WHERE document_id = ?

                """,

                (

                    document_id,

                )

            )


            connection.commit()


            return cursor.rowcount > 0


    # ========================================================
    # DELETE USER DOCUMENT
    # ========================================================

    def delete_user_document(

        self,

        document_id: str,

        user_id: int

    ):

        """
        Delete a document only if it belongs
        to the authenticated user.
        """

        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                DELETE FROM documents

                WHERE

                    document_id = ?

                    AND user_id = ?

                """,

                (

                    document_id,

                    user_id

                )

            )


            connection.commit()


            return cursor.rowcount > 0


    # ========================================================
    # SEARCH DOCUMENTS
    # ========================================================

    def search_documents(

        self,

        keyword: str

    ):

        keyword = keyword.strip()


        if not keyword:

            return []


        search_pattern = (

            f"%{keyword}%"

        )


        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                SELECT *

                FROM documents

                WHERE

                    filename LIKE ?

                    OR file_type LIKE ?

                    OR document_id LIKE ?

                ORDER BY created_at DESC

                """,

                (

                    search_pattern,

                    search_pattern,

                    search_pattern

                )

            )


            rows = cursor.fetchall()


        return [

            dict(

                row

            )

            for row in rows

        ]


    # ========================================================
    # SEARCH USER DOCUMENTS
    # ========================================================

    def search_user_documents(

        self,

        keyword: str,

        user_id: int

    ):

        """
        Search only documents belonging
        to the authenticated user.
        """

        keyword = keyword.strip()


        if not keyword:

            return []


        search_pattern = (

            f"%{keyword}%"

        )


        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                SELECT *

                FROM documents

                WHERE

                    user_id = ?

                    AND (

                        filename LIKE ?

                        OR file_type LIKE ?

                        OR document_id LIKE ?

                    )

                ORDER BY created_at DESC

                """,

                (

                    user_id,

                    search_pattern,

                    search_pattern,

                    search_pattern

                )

            )


            rows = cursor.fetchall()


        return [

            dict(

                row

            )

            for row in rows

        ]


    # ========================================================
    # COUNT DOCUMENTS
    # ========================================================

    def count_documents(

        self

    ):

        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                SELECT COUNT(*)

                FROM documents

                """

            )


            result = cursor.fetchone()


        return result[0]


    # ========================================================
    # COUNT USER DOCUMENTS
    # ========================================================

    def count_user_documents(

        self,

        user_id: int

    ):

        """
        Count only documents belonging
        to the authenticated user.
        """

        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                SELECT COUNT(*)

                FROM documents

                WHERE user_id = ?

                """,

                (

                    user_id,

                )

            )


            result = cursor.fetchone()


        return result[0]