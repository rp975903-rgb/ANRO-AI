from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from pydantic import (
    BaseModel,
    EmailStr,
)

from app.auth.auth_service import (
    AuthService,
)

from app.auth.dependencies import (
    get_current_user,
)


# ============================================================
# API ROUTER
# ============================================================

router = APIRouter(

    prefix="/api/auth",

    tags=[
        "Authentication"
    ],

)


# ============================================================
# AUTHENTICATION SERVICE
# ============================================================

auth_service = AuthService()


# ============================================================
# REGISTER REQUEST
# ============================================================

class RegisterRequest(BaseModel):

    full_name: str

    email: EmailStr

    password: str


# ============================================================
# LOGIN REQUEST
# ============================================================

class LoginRequest(BaseModel):

    email: EmailStr

    password: str


# ============================================================
# REGISTER USER
# ============================================================

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
def register_user(

    request: RegisterRequest,

):

    """
    Register a new ANRO AI user.
    """

    try:

        user = auth_service.register_user(

            full_name=request.full_name,

            email=str(
                request.email
            ),

            password=request.password,

        )


        return {

            "success": True,

            "message":
                "User registered successfully.",

            "user":
                user,

        }


    except ValueError as error:

        raise HTTPException(

            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),

            detail=str(
                error
            ),

        )


    except Exception as error:

        raise HTTPException(

            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),

            detail=(
                "Failed to register user. "
                f"Error: {str(error)}"
            ),

        )


# ============================================================
# LOGIN USER
# ============================================================

@router.post(
    "/login",
)
def login_user(

    request: LoginRequest,

):

    """
    Authenticate user and return JWT access token.
    """

    try:

        result = auth_service.login_user(

            email=str(
                request.email
            ),

            password=request.password,

        )


        return {

            "success": True,

            "message":
                "Login successful.",

            **result,

        }


    except ValueError as error:

        raise HTTPException(

            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),

            detail=str(
                error
            ),

            headers={

                "WWW-Authenticate":
                    "Bearer",

            },

        )


    except Exception as error:

        raise HTTPException(

            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),

            detail=(
                "Failed to login user. "
                f"Error: {str(error)}"
            ),

        )


# ============================================================
# GET CURRENT USER
# ============================================================

@router.get(
    "/me",
)
def get_current_user_info(

    current_user: dict = Depends(

        get_current_user

    ),

):

    """
    Return the currently authenticated user.
    """

    return {

        "success": True,

        "user": {

            "user_id":
                current_user.get(
                    "user_id"
                ),

            "email":
                current_user.get(
                    "email"
                ),

            "full_name":
                current_user.get(
                    "full_name"
                ),

            "is_active":
                bool(
                    current_user.get(
                        "is_active",
                        True
                    )
                ),

            "created_at":
                current_user.get(
                    "created_at"
                ),

        },

    }


# ============================================================
# AUTHENTICATION STATUS
# ============================================================

@router.get(
    "/status",
)
def auth_status():

    """
    Return authentication service status.
    """

    try:

        return {

            "success": True,

            **auth_service.get_status(),

        }


    except Exception as error:

        raise HTTPException(

            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),

            detail=str(
                error
            ),

        )