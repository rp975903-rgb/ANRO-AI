from typing import Any

from app.auth.user_database import (
    UserDatabase,
)

from app.auth.password_handler import (
    hash_password,
    verify_password,
)

from app.auth.jwt_handler import (
    create_access_token,
)

# ============================================================
# AUTHENTICATION SERVICE
# ============================================================

class AuthService:
    """
    Authentication service for ANRO AI.

    Uses the existing UserDatabase as the
    single source of truth for authentication.

    Responsibilities:

    - Register users
    - Hash passwords
    - Verify passwords
    - Authenticate users
    - Generate JWT access tokens
    - Get users by ID
    - Get users by email
    """

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        db: UserDatabase | None = None,
    ):
        self.db = db or UserDatabase()

    # ========================================================
    # REGISTER USER
    # ========================================================

    def register_user(
        self,
        full_name: str,
        email: str,
        password: str,
    ) -> dict[str, Any]:
        # ====================================================
        # VALIDATE NAME
        # ====================================================
        full_name = (
            full_name or ""
        ).strip()

        if not full_name:
            raise ValueError(
                "Full name cannot be empty."
            )

        # ====================================================
        # VALIDATE EMAIL
        # ====================================================
        email = (
            email or ""
        ).strip().lower()

        if not email:
            raise ValueError(
                "Email cannot be empty."
            )

        # ====================================================
        # VALIDATE PASSWORD
        # ====================================================
        if not password:
            raise ValueError(
                "Password cannot be empty."
            )

        if len(password) < 6:
            raise ValueError(
                "Password must contain "
                "at least 6 characters."
            )

        # ====================================================
        # CHECK EXISTING USER
        # ========================================================
        if self.db.email_exists(
            email
        ):
            raise ValueError(
                "A user with this email "
                "already exists."
            )

        # ====================================================
        # HASH PASSWORD
        # ========================================================
        hashed_password = hash_password(
            password
        )

        # ====================================================
        # CREATE USER
        # ========================================================
        user = self.db.create_user(
            full_name=full_name,
            email=email,
            hashed_password=hashed_password,
        )

        # ====================================================
        # RETURN SAFE USER DATA
        # ========================================================
        return {
            "user_id": user["user_id"],
            "full_name": user["full_name"],
            "email": user["email"],
            "is_active": bool(user["is_active"]),
            "created_at": user["created_at"],
        }

    # ========================================================
    # AUTHENTICATE USER
    # ========================================================

    def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> dict | None:
        # ====================================================
        # NORMALIZE EMAIL
        # ====================================================
        email = (
            email or ""
        ).strip().lower()

        # ====================================================
        # FIND USER
        # ========================================================
        user = self.db.get_user_by_email(
            email
        )

        if user is None:
            return None

        # ====================================================
        # CHECK ACTIVE STATUS
        # ====================================================
        if not bool(
            user.get(
                "is_active",
                0
            )
        ):
            return None

        # ====================================================
        # VERIFY PASSWORD
        # ========================================================
        password_valid = verify_password(
            password,
            user.get(
                "hashed_password",
                ""
            ),
        )

        if not password_valid:
            return None

        # ====================================================
        # AUTHENTICATION SUCCESS
        # ========================================================
        return user

    # ========================================================
    # LOGIN USER
    # ========================================================

    def login_user(
        self,
        email: str,
        password: str,
    ) -> dict[str, Any]:
        # ====================================================
        # AUTHENTICATE USER
        # ====================================================
        user = self.authenticate_user(
            email=email,
            password=password,
        )

        if user is None:
            raise ValueError(
                "Invalid email or password."
            )

        # ====================================================
        # CREATE JWT TOKEN
        # ========================================================
        access_token = create_access_token(
            data={
                "sub": str(user["user_id"]),
                "email": user["email"],
                "full_name": user["full_name"],
            }
        )

        # ====================================================
        # RETURN LOGIN RESPONSE
        # ========================================================
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "user_id": user["user_id"],
                "full_name": user["full_name"],
                "email": user["email"],
                "is_active": bool(user["is_active"]),
            },
        }

    # ========================================================
    # GET USER BY ID
    # ========================================================

    def get_user_by_id(
        self,
        user_id: int,
    ) -> dict | None:
        return self.db.get_user_by_id(
            user_id
        )

    # ========================================================
    # GET USER BY EMAIL
    # ========================================================

    def get_user_by_email(
        self,
        email: str,
    ) -> dict | None:
        email = (
            email or ""
        ).strip().lower()
        return self.db.get_user_by_email(
            email
        )

    # ========================================================
    # GET AUTH SERVICE STATUS
    # ========================================================

    def get_status(
        self,
    ) -> dict[str, Any]:
        return {
            "service": "AuthService",
            "database": "SQLite / UserDatabase",
            "database_path": str(
                self.db.database_path
            ),
            "password_hashing": "bcrypt",
            "jwt_enabled": True,
            "user_count": self.db.count_users(),
            "ready": True,
        }

