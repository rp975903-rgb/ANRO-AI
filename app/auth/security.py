from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from app.auth.jwt_handler import (
    decode_access_token
)

from app.auth.user_database import (
    UserDatabase
)


# ========================================================
# HTTP BEARER SECURITY
# ========================================================

security = HTTPBearer()


# ========================================================
# USER DATABASE
# ========================================================

user_database = UserDatabase()


# ========================================================
# GET CURRENT USER
# ========================================================

def get_current_user(

    credentials: HTTPAuthorizationCredentials = Depends(

        security

    )

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
    Get User ID
            ↓
    Find User in Database
            ↓
    Return User
    """


    # ====================================================
    # GET ACCESS TOKEN
    # ====================================================

    token = (

        credentials.credentials

    )


    if not token:

        raise HTTPException(

            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),

            detail="Authentication token is missing.",

            headers={

                "WWW-Authenticate":

                    "Bearer"

            }

        )


    # ====================================================
    # DECODE JWT TOKEN
    # ====================================================

    payload = (

        decode_access_token(

            token

        )

    )


    if payload is None:

        raise HTTPException(

            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),

            detail="Invalid or expired authentication token.",

            headers={

                "WWW-Authenticate":

                    "Bearer"

            }

        )


    # ====================================================
    # GET USER ID FROM TOKEN
    # ====================================================

    user_id = (

        payload.get(

            "sub"

        )

    )


    if user_id is None:

        raise HTTPException(

            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),

            detail="Invalid token payload.",

            headers={

                "WWW-Authenticate":

                    "Bearer"

            }

        )


    # ====================================================
    # CONVERT USER ID
    # ====================================================

    try:

        user_id = int(

            user_id

        )

    except (

        ValueError,

        TypeError

    ):

        raise HTTPException(

            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),

            detail="Invalid user ID in token.",

            headers={

                "WWW-Authenticate":

                    "Bearer"

            }

        )


    # ====================================================
    # FIND USER IN DATABASE
    # ====================================================

    user = (

        user_database

        .get_user_by_id(

            user_id

        )

    )


    if user is None:

        raise HTTPException(

            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),

            detail="User not found.",

            headers={

                "WWW-Authenticate":

                    "Bearer"

            }

        )


    # ====================================================
    # CHECK USER ACTIVE STATUS
    # ====================================================

    if not user["is_active"]:

        raise HTTPException(

            status_code=(
                status.HTTP_403_FORBIDDEN
            ),

            detail="User account is inactive."

        )


    # ====================================================
    # RETURN SAFE USER INFORMATION
    # ====================================================

    return {

        "sub":

            str(

                user["user_id"]

            ),

        "user_id":

            user["user_id"],

        "email":

            user["email"],

        "full_name":

            user["full_name"],

        "is_active":

            bool(

                user["is_active"]

            )

    }