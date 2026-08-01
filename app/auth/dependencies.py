from fastapi import (
    Depends,
    HTTPException,
    status,
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

from app.auth.jwt_handler import (
    decode_access_token,
)

from app.auth.user_database import (
    UserDatabase,
)


# ============================================================
# HTTP BEARER SECURITY
# ============================================================

security = HTTPBearer(
    auto_error=False
)


# ============================================================
# USER DATABASE
# ============================================================

user_database = UserDatabase()


# ============================================================
# GET CURRENT AUTHENTICATED USER
# ============================================================

def get_current_user(

    credentials: HTTPAuthorizationCredentials | None = Depends(

        security

    ),

) -> dict:

    """
    Get the currently authenticated user.

    Flow:

    Authorization Header
            ↓
    Bearer Token
            ↓
    Decode JWT
            ↓
    Extract User ID
            ↓
    Find User in UserDatabase
            ↓
    Check Account Status
            ↓
    Return User Dictionary
    """


    # ========================================================
    # CHECK AUTHORIZATION HEADER
    # ========================================================

    if credentials is None:

        raise HTTPException(

            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),

            detail=(
                "Authentication token is required."
            ),

            headers={
                "WWW-Authenticate": "Bearer"
            },

        )


    # ========================================================
    # GET TOKEN
    # ========================================================

    token = credentials.credentials


    if not token:

        raise HTTPException(

            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),

            detail=(
                "Authentication token is missing."
            ),

            headers={
                "WWW-Authenticate": "Bearer"
            },

        )


    # ========================================================
    # DECODE JWT
    # ========================================================

    payload = decode_access_token(

        token

    )


    if payload is None:

        raise HTTPException(

            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),

            detail=(
                "Invalid or expired authentication token."
            ),

            headers={
                "WWW-Authenticate": "Bearer"
            },

        )


    # ========================================================
    # GET USER ID FROM JWT
    # ========================================================

    user_id = payload.get(

        "sub"

    )


    if user_id is None:

        raise HTTPException(

            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),

            detail=(
                "Invalid authentication token payload."
            ),

            headers={
                "WWW-Authenticate": "Bearer"
            },

        )


    # ========================================================
    # CONVERT USER ID
    # ========================================================

    try:

        user_id = int(

            user_id

        )

    except (

        TypeError,

        ValueError,

    ):

        raise HTTPException(

            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),

            detail=(
                "Invalid user ID in authentication token."
            ),

            headers={
                "WWW-Authenticate": "Bearer"
            },

        )


    # ========================================================
    # FIND USER IN USER DATABASE
    # ========================================================

    user = user_database.get_user_by_id(

        user_id

    )


    # ========================================================
    # USER NOT FOUND
    # ========================================================

    if user is None:

        raise HTTPException(

            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),

            detail=(
                "Authenticated user not found."
            ),

            headers={
                "WWW-Authenticate": "Bearer"
            },

        )


    # ========================================================
    # CHECK ACCOUNT STATUS
    # ========================================================

    if not bool(

        user.get(

            "is_active",

            0

        )

    ):

        raise HTTPException(

            status_code=(
                status.HTTP_403_FORBIDDEN
            ),

            detail=(
                "User account is inactive."
            ),

        )


    # ========================================================
    # RETURN CURRENT USER
    # ========================================================

    return user