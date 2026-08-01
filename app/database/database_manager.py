import sqlite3
from pathlib import Path

from app.config import DATABASE_PATH


class DatabaseManager:
    """
    Central SQLite database manager.

    Responsible for:

    - Database connection
    - Table creation
    - Query execution
    - Insert operations
    - Update operations
    - Delete operations
    """


    def __init__(
        self,
        database_path: str | Path = DATABASE_PATH
    ):
        """
        Initialize database manager.
        """

        self.database_path = Path(
            database_path
        )

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )


    def get_connection(self):
        """
        Create and return a SQLite connection.
        """

        connection = sqlite3.connect(

            str(
                self.database_path
            )

        )

        connection.row_factory = (
            sqlite3.Row
        )

        return connection


    def initialize_database(self):
        """
        Create all required database tables.
        """

        connection = (
            self.get_connection()
        )

        cursor = (
            connection.cursor()
        )


        # ====================================================
        # DOCUMENTS TABLE
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                document_id TEXT UNIQUE NOT NULL,

                filename TEXT NOT NULL,

                file_type TEXT,

                file_path TEXT,

                total_chunks INTEGER DEFAULT 0,

                status TEXT DEFAULT 'processed',

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
            """
        )


        # ====================================================
        # DATASETS TABLE
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS datasets (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                dataset_id TEXT UNIQUE NOT NULL,

                filename TEXT NOT NULL,

                file_type TEXT,

                file_path TEXT,

                rows_count INTEGER DEFAULT 0,

                columns_count INTEGER DEFAULT 0,

                status TEXT DEFAULT 'loaded',

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
            """
        )


        # ====================================================
        # AI EXECUTION HISTORY
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ai_executions (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                execution_id TEXT UNIQUE NOT NULL,

                user_query TEXT NOT NULL,

                agent_name TEXT,

                response TEXT,

                status TEXT DEFAULT 'completed',

                execution_time REAL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
            """
        )


        connection.commit()

        connection.close()


    def execute(
        self,
        query: str,
        parameters: tuple = ()
    ):
        """
        Execute a database query.

        Used for:

        INSERT
        UPDATE
        DELETE
        """

        connection = (
            self.get_connection()
        )

        cursor = (
            connection.cursor()
        )


        cursor.execute(

            query,

            parameters

        )


        connection.commit()


        last_id = (
            cursor.lastrowid
        )


        connection.close()


        return last_id


    def fetch_one(
        self,
        query: str,
        parameters: tuple = ()
    ):
        """
        Fetch one database record.
        """

        connection = (
            self.get_connection()
        )

        cursor = (
            connection.cursor()
        )


        cursor.execute(

            query,

            parameters

        )


        row = (
            cursor.fetchone()
        )


        connection.close()


        if row:

            return dict(
                row
            )


        return None


    def fetch_all(
        self,
        query: str,
        parameters: tuple = ()
    ):
        """
        Fetch multiple database records.
        """

        connection = (
            self.get_connection()
        )

        cursor = (
            connection.cursor()
        )


        cursor.execute(

            query,

            parameters

        )


        rows = (
            cursor.fetchall()
        )


        connection.close()


        return [

            dict(
                row
            )

            for row in rows

        ]