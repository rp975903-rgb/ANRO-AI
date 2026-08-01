from app.auth.security import (
    hash_password,
    verify_password,
)


print("=" * 60)
print("🔐 ANRO AI SECURITY TEST")
print("=" * 60)


password = "ANRO@12345"


print()
print("🔄 Hashing password...")


hashed_password = hash_password(
    password
)


print()
print("✅ Password hashed successfully.")


print()
print("🔐 Hashed Password:")

print(
    hashed_password
)


print()
print("🔄 Verifying correct password...")


result = verify_password(
    password,
    hashed_password
)


if result:

    print(
        "✅ Correct password verification successful."
    )

else:

    print(
        "❌ Correct password verification failed."
    )


print()
print("🔄 Testing wrong password...")


wrong_result = verify_password(
    "WrongPassword123",
    hashed_password
)


if not wrong_result:

    print(
        "✅ Wrong password correctly rejected."
    )

else:

    print(
        "❌ Security error: wrong password accepted."
    )


print()
print("=" * 60)
print("🎉 SECURITY TEST COMPLETED")
print("=" * 60)