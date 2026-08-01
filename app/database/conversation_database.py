from pathlib import Path
import sqlite3
from datetime import datetime


class ConversationDatabase:
    """
    SQLite database for persistent conversation memory.

    Stores:

    - Conversation ID
    - Message ID
    - Role
    - Message content
    - Created time
    """

    def __init__(
        self,
        database_path: str | Path = (
            "data/metadata/conversations.db"
        )
    ):

        self.database_path = Path(
            database_path
        )

        # Create parent directory

        self.database_path.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        # Initialize database

        self.create_table()


    # ========================================================
    # DATABASE CONNECTION
    # ========================================================

    def get_connection(self):

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

    def create_table(self):

        with self.get_connection() as connection:

            connection.execute(

                """
                CREATE TABLE IF NOT EXISTS
                conversation_messages (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    conversation_id TEXT NOT NULL,

                    role TEXT NOT NULL,

                    content TEXT NOT NULL,

                    created_at TEXT NOT NULL

                )
                """

            )

            connection.commit()


    # ========================================================
    # ADD MESSAGE
    # ========================================================

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str
    ):

        if not conversation_id.strip():

            raise ValueError(

                "Conversation ID cannot be empty."

            )


        if not role.strip():

            raise ValueError(

                "Role cannot be empty."

            )


        if not content.strip():

            raise ValueError(

                "Content cannot be empty."

            )


        created_at = (

            datetime.now()

            .isoformat(

                timespec="seconds"

            )

        )


        with self.get_connection() as connection:

            cursor = connection.execute(

                """
                INSERT INTO conversation_messages (

                    conversation_id,

                    role,

                    content,

                    created_at

                )

                VALUES (?, ?, ?, ?)
                """,

                (

                    conversation_id,

                    role,

                    content,

                    created_at

                )

            )


            connection.commit()


            return cursor.lastrowid


    # ========================================================
    # GET CONVERSATION
    # ========================================================

    def get_conversation(
        self,
        conversation_id: str
    ):

        with self.get_connection() as connection:

            cursor = connection.execute(

                """
                SELECT

                    id,

                    conversation_id,

                    role,

                    content,

                    created_at

                FROM conversation_messages

                WHERE conversation_id = ?

                ORDER BY id ASC
                """,

                (

                    conversation_id,

                )

            )


            rows = cursor.fetchall()


        return [

            dict(row)

            for row in rows

        ]


    # ========================================================
    # GET RECENT MESSAGES
    # ========================================================

    def get_recent_messages(
        self,
        conversation_id: str,
        limit: int = 10
    ):

        if limit <= 0:

            raise ValueError(

                "Limit must be greater than zero."

            )


        with self.get_connection() as connection:

            cursor = connection.execute(

                """
                SELECT

                    id,

                    conversation_id,

                    role,

                    content,

                    created_at

                FROM conversation_messages

                WHERE conversation_id = ?

                ORDER BY id DESC

                LIMIT ?
                """,

                (

                    conversation_id,

                    limit

                )

            )


            rows = cursor.fetchall()


        messages = [

            dict(row)

            for row in rows

        ]


        # Reverse so oldest appears first

        messages.reverse()


        return messages


    # ========================================================
    # DELETE CONVERSATION
    # ========================================================

    def delete_conversation(
        self,
        conversation_id: str
    ):

        with self.get_connection() as connection:

            cursor = connection.execute(

                """
                DELETE FROM conversation_messages

                WHERE conversation_id = ?
                """,

                (

                    conversation_id,

                )

            )


            connection.commit()


            return cursor.rowcount > 0


    # ========================================================
    # COUNT MESSAGES
    # ========================================================

    def count_messages(
        self,
        conversation_id: str
    ):

        with self.get_connection() as connection:

            cursor = connection.execute(

                """
                SELECT COUNT(*)

                FROM conversation_messages

                WHERE conversation_id = ?
                """,

                (

                    conversation_id,

                )

            )


            result = cursor.fetchone()


        return result[0]