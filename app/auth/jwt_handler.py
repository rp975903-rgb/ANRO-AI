import os

from datetime import (
    datetime,
    timedelta,
    timezone,
)

from typing import Any

from jose import (
    JWTError,
    jwt,
)

from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# JWT CONFIGURATION
# ============================================================

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY"
)

JWT_ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256",
)

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(

    os.getenv(

        "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",

        "60",

    )

)


# ============================================================
# VALIDATE JWT SECRET
# ============================================================

if not JWT_SECRET_KEY:

    raise RuntimeError(

        "JWT_SECRET_KEY is missing. "
        "Please add JWT_SECRET_KEY to your .env file."

    )


# ============================================================
# CREATE ACCESS TOKEN
# ============================================================

def create_access_token(

    data: dict[str, Any],

    expires_delta: timedelta | None = None,

) -> str:

    """
    Create a JWT access token.

    The user's database ID is stored
    inside the JWT 'sub' claim.
    """

    # ========================================================
    # COPY DATA
    # ========================================================

    to_encode = data.copy()


    # ========================================================
    # CALCULATE EXPIRATION
    # ========================================================

    if expires_delta is not None:

        expire = (

            datetime.now(timezone.utc)

            + expires_delta

        )

    else:

        expire = (

            datetime.now(timezone.utc)

            + timedelta(

                minutes=(
                    JWT_ACCESS_TOKEN_EXPIRE_MINUTES
                )

            )

        )


    # ========================================================
    # ADD EXPIRATION
    # ========================================================

    to_encode.update(

        {
            "exp": expire
        }

    )


    # ========================================================
    # CREATE JWT
    # ========================================================

    encoded_jwt = jwt.encode(

        to_encode,

        JWT_SECRET_KEY,

        algorithm=JWT_ALGORITHM,

    )


    return encoded_jwt


# ============================================================
# DECODE ACCESS TOKEN
# ============================================================

def decode_access_token(

    token: str,

) -> dict[str, Any] | None:

    """
    Decode and validate JWT access token.

    Returns:
        Dictionary payload if valid.
        None if invalid or expired.
    """

    try:

        payload = jwt.decode(

            token,

            JWT_SECRET_KEY,

            algorithms=[
                JWT_ALGORITHM
            ],

        )

        return payload


    except JWTError:

        return None