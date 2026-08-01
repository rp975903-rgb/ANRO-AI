from app.auth.database import (
    init_database,
    SessionLocal,
)

from app.auth.models import User


print("=" * 60)
print("🗄️ ANRO AI AUTH DATABASE TEST")
print("=" * 60)


print()
print("🔄 Initializing authentication database...")


init_database()


print(
    "✅ Database initialized successfully."
)


print()
print("🔄 Testing database connection...")


db = SessionLocal()


try:

    user_count = (
        db.query(User)
        .count()
    )


    print()
    print(
        "✅ Database connection successful."
    )


    print()
    print(
        f"👤 Users currently registered: "
        f"{user_count}"
    )


finally:

    db.close()


print()
print("=" * 60)
print("🎉 AUTH DATABASE TEST COMPLETED")
print("=" * 60)