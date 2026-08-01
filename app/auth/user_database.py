from pathlib import Path
import sqlite3
from datetime import datetime


class UserDatabase:
    """
    SQLite database for ANRO AI users.

    Stores:

    - User ID
    - Full name
    - Email
    - Hashed password
    - Active status
    - Created time
    - Updated time
    """


    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        database_path: str | Path = (
            "data/auth/users.db"
        )
    ):

        self.database_path = Path(
            database_path
        )


        # ====================================================
        # CREATE DATABASE DIRECTORY
        # ====================================================

        self.database_path.parent.mkdir(

            parents=True,

            exist_ok=True

        )


        # ====================================================
        # CREATE USERS TABLE
        # ====================================================

        self.create_table()


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


        # Return rows as dictionary-like objects

        connection.row_factory = (

            sqlite3.Row

        )


        return connection


    # ========================================================
    # CREATE USERS TABLE
    # ========================================================

    def create_table(
        self
    ):

        sql_query = """

        CREATE TABLE IF NOT EXISTS users (

            user_id INTEGER PRIMARY KEY AUTOINCREMENT,

            full_name TEXT NOT NULL,

            email TEXT NOT NULL UNIQUE,

            hashed_password TEXT NOT NULL,

            is_active INTEGER DEFAULT 1,

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
    # CREATE USER
    # ========================================================

    def create_user(

        self,

        full_name: str,

        email: str,

        hashed_password: str

    ) -> dict:

        """
        Create a new user.
        """

        now = datetime.now().isoformat(

            timespec="seconds"

        )


        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                INSERT INTO users (

                    full_name,

                    email,

                    hashed_password,

                    is_active,

                    created_at,

                    updated_at

                )

                VALUES (?, ?, ?, ?, ?, ?)

                """,

                (

                    full_name,

                    email,

                    hashed_password,

                    1,

                    now,

                    now

                )

            )


            connection.commit()


            user_id = cursor.lastrowid


        return self.get_user_by_id(

            user_id

        )


    # ========================================================
    # GET USER BY ID
    # ========================================================

    def get_user_by_id(

        self,

        user_id: int

    ) -> dict | None:

        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                SELECT *

                FROM users

                WHERE user_id = ?

                LIMIT 1

                """,

                (

                    user_id,

                )

            )


            row = cursor.fetchone()


        if row:

            return dict(

                row

            )


        return None


    # ========================================================
    # GET USER BY EMAIL
    # ========================================================

    def get_user_by_email(

        self,

        email: str

    ) -> dict | None:

        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                SELECT *

                FROM users

                WHERE email = ?

                LIMIT 1

                """,

                (

                    email,

                )

            )


            row = cursor.fetchone()


        if row:

            return dict(

                row

            )


        return None


    # ========================================================
    # CHECK EMAIL EXISTS
    # ========================================================

    def email_exists(

        self,

        email: str

    ) -> bool:

        user = self.get_user_by_email(

            email

        )


        return user is not None


    # ========================================================
    # UPDATE USER ACTIVE STATUS
    # ========================================================

    def update_active_status(

        self,

        user_id: int,

        is_active: bool

    ) -> bool:

        now = datetime.now().isoformat(

            timespec="seconds"

        )


        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                UPDATE users

                SET

                    is_active = ?,

                    updated_at = ?

                WHERE user_id = ?

                """,

                (

                    1 if is_active else 0,

                    now,

                    user_id

                )

            )


            connection.commit()


            return cursor.rowcount > 0


    # ========================================================
    # DELETE USER
    # ========================================================

    def delete_user(

        self,

        user_id: int

    ) -> bool:

        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                DELETE FROM users

                WHERE user_id = ?

                """,

                (

                    user_id,

                )

            )


            connection.commit()


            return cursor.rowcount > 0


    # ========================================================
    # COUNT USERS
    # ========================================================

    def count_users(

        self

    ) -> int:

        with self.get_connection() as connection:

            cursor = connection.execute(

                """

                SELECT COUNT(*)

                FROM users

                """

            )


            result = cursor.fetchone()


        return result[0]