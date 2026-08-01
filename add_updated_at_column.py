import sqlite3

from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = (

    Path(__file__)
    .resolve()
)


# ============================================================
# DATABASE PATH
# ============================================================

DATABASE_PATH = (

    PROJECT_ROOT
    / "data"
    / "anro_ai.db"

)


print()
print("=" * 60)
print("ANRO AI DATABASE MIGRATION")
print("=" * 60)

print(
    f"Database: {DATABASE_PATH}"
)


# ============================================================
# CHECK DATABASE
# ============================================================

if not DATABASE_PATH.exists():

    print()

    print(
        "❌ Database file not found."
    )

    print(
        f"Expected: {DATABASE_PATH}"
    )

    raise SystemExit(1)


# ============================================================
# CONNECT DATABASE
# ============================================================

connection = sqlite3.connect(

    DATABASE_PATH

)


cursor = connection.cursor()


# ============================================================
# CHECK USERS TABLE
# ============================================================

cursor.execute(

    """
    PRAGMA table_info(users)
    """

)


columns = cursor.fetchall()


column_names = [

    column[1]

    for column in columns

]


print()

print(
    "Existing users columns:"
)

for column in column_names:

    print(
        f"  - {column}"
    )


# ============================================================
# ADD UPDATED_AT COLUMN
# ============================================================

if "updated_at" not in column_names:

    print()

    print(
        "🔄 Adding updated_at column..."
    )


    cursor.execute(

        """
        ALTER TABLE users
        ADD COLUMN updated_at DATETIME
        """

    )


    # ========================================================
    # SET EXISTING USERS UPDATED TIME
    # ========================================================

    cursor.execute(

        """
        UPDATE users
        SET updated_at = created_at
        WHERE updated_at IS NULL
        """

    )


    connection.commit()


    print(
        "✅ updated_at column added successfully."
    )


else:

    print()

    print(
        "✅ updated_at column already exists."
    )


# ============================================================
# CLOSE DATABASE
# ============================================================

connection.close()


print()

print("=" * 60)

print(
    "✅ DATABASE MIGRATION COMPLETED"
)

print("=" * 60)

print()