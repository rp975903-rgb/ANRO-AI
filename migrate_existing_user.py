from datetime import datetime

from app.auth.database import (
    SessionLocal,
    init_database,
)

from app.auth.models import (
    User,
)

from app.auth.user_database import (
    UserDatabase,
)


# ============================================================
# MIGRATE EXISTING USER
# ============================================================

def migrate_user():

    print()
    print("=" * 60)
    print("🔄 ANRO AI USER MIGRATION")
    print("=" * 60)


    # ========================================================
    # INITIALIZE SQLALCHEMY DATABASE
    # ========================================================

    init_database()

    print(
        "✅ SQLAlchemy database initialized."
    )


    # ========================================================
    # GET OLD USER DATABASE
    # ========================================================

    old_database = UserDatabase()

    old_user = (

        old_database

        .get_user_by_email(

            "rp975903@gmail.com"

        )

    )


    if old_user is None:

        print(
            "❌ Existing user not found."
        )

        return


    print(
        "✅ Existing user found:"
    )

    print(
        old_user
    )


    # ========================================================
    # CREATE SQLALCHEMY SESSION
    # ========================================================

    db = SessionLocal()


    try:

        # ====================================================
        # CHECK IF USER ALREADY EXISTS
        # ====================================================

        existing_user = (

            db

            .query(User)

            .filter(

                User.email == old_user["email"]

            )

            .first()

        )


        if existing_user:

            print()

            print(
                "⚠️ User already exists "
                "in SQLAlchemy database."
            )

            print(
                f"User ID: {existing_user.id}"
            )

            return


        # ====================================================
        # CONVERT CREATED DATE
        # ====================================================

        created_at = datetime.fromisoformat(

            old_user["created_at"]

        )


        # ====================================================
        # CONVERT UPDATED DATE
        # ====================================================

        updated_at = datetime.fromisoformat(

            old_user["updated_at"]

        )


        # ====================================================
        # CREATE SQLALCHEMY USER
        # ====================================================

        user = User(

            id=old_user["user_id"],

            full_name=old_user["full_name"],

            email=old_user["email"],

            password_hash=(

                old_user["hashed_password"]

            ),

            created_at=created_at,

            updated_at=updated_at,

            is_active=bool(

                old_user["is_active"]

            ),

        )


        # ====================================================
        # SAVE USER
        # ====================================================

        db.add(user)

        db.commit()

        db.refresh(user)


        # ====================================================
        # SUCCESS
        # ====================================================

        print()

        print("=" * 60)

        print(
            "🎉 USER MIGRATION SUCCESSFUL"
        )

        print("=" * 60)

        print(
            f"User ID     : {user.id}"
        )

        print(
            f"Full Name   : {user.full_name}"
        )

        print(
            f"Email       : {user.email}"
        )

        print(
            f"Active      : {user.is_active}"
        )

        print()

        print(
            "✅ Existing bcrypt password hash preserved."
        )

        print(
            "✅ Existing password does NOT need to be changed."
        )

        print()

    except Exception as error:

        db.rollback()

        print()

        print(
            "❌ Migration failed."
        )

        print(
            f"Error: {error}"
        )

        raise

    finally:

        db.close()


# ============================================================
# RUN MIGRATION
# ============================================================

if __name__ == "__main__":

    migrate_user()