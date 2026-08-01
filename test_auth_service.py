from app.auth.database import (
    init_database,
    SessionLocal,
)

from app.auth.auth_service import (
    create_user,
    get_user_by_email,
    authenticate_user,
)


# ============================================================
# TEST CONFIGURATION
# ============================================================

TEST_NAME = "Rohit Prajapati"

TEST_EMAIL = "rohit.test@anro.ai"

TEST_PASSWORD = "TestPassword@123"


# ============================================================
# START TEST
# ============================================================

print("=" * 60)

print(
    "🔐 ANRO AI AUTHENTICATION SERVICE TEST"
)

print("=" * 60)


# ============================================================
# INITIALIZE DATABASE
# ============================================================

print()

print(
    "🔄 Initializing database..."
)


init_database()


print(
    "✅ Database ready."
)


# ============================================================
# CREATE DATABASE SESSION
# ============================================================

db = SessionLocal()


try:

    # ========================================================
    # CHECK EXISTING USER
    # ========================================================

    existing_user = get_user_by_email(

        db,

        TEST_EMAIL,

    )


    if existing_user:

        print()

        print(
            "ℹ️ Test user already exists."
        )

        user = existing_user


    else:

        # ====================================================
        # CREATE NEW USER
        # ====================================================

        print()

        print(
            "🔄 Creating test user..."
        )


        user = create_user(

            db,

            TEST_NAME,

            TEST_EMAIL,

            TEST_PASSWORD,

        )


        if user:

            print()

            print(
                "✅ User created successfully."
            )

        else:

            print()

            print(
                "❌ User creation failed."
            )


    # ========================================================
    # DISPLAY USER
    # ========================================================

    if user:

        print()

        print(
            "👤 User Information"
        )

        print(
            f"ID: {user.id}"
        )

        print(
            f"Name: {user.full_name}"
        )

        print(
            f"Email: {user.email}"
        )

        print(
            f"Active: {user.is_active}"
        )


    # ========================================================
    # TEST CORRECT LOGIN
    # ========================================================

    print()

    print(
        "🔄 Testing correct password..."
    )


    authenticated_user = authenticate_user(

        db,

        TEST_EMAIL,

        TEST_PASSWORD,

    )


    if authenticated_user:

        print(
            "✅ Correct login successful."
        )

    else:

        print(
            "❌ Correct login failed."
        )


    # ========================================================
    # TEST WRONG PASSWORD
    # ========================================================

    print()

    print(
        "🔄 Testing wrong password..."
    )


    wrong_login = authenticate_user(

        db,

        TEST_EMAIL,

        "WrongPassword@123",

    )


    if wrong_login is None:

        print(
            "✅ Wrong password correctly rejected."
        )

    else:

        print(
            "❌ SECURITY ERROR: Wrong password accepted!"
        )


finally:

    db.close()


# ============================================================
# TEST COMPLETE
# ============================================================

print()

print("=" * 60)

print(
    "🎉 AUTHENTICATION SERVICE TEST COMPLETED"
)

print("=" * 60)