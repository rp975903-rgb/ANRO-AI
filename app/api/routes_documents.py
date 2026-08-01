from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends,
)

from app.document_processing.document_ingestion_manager import (
    DocumentIngestionManager,
)

from app.auth.dependencies import (
    get_current_user,
)


# ============================================================
# API ROUTER
# ============================================================

router = APIRouter(

    prefix="/api/documents",

    tags=[
        "Documents"
    ],

)


# ============================================================
# DOCUMENT INGESTION MANAGER
# ============================================================

ingestion_manager = (

    DocumentIngestionManager()

)


# ============================================================
# DOCUMENT DIRECTORY
# ============================================================

DOCUMENT_DIRECTORY = Path(

    "data/documents"

)


DOCUMENT_DIRECTORY.mkdir(

    parents=True,

    exist_ok=True,

)


# ============================================================
# SUPPORTED FILE EXTENSIONS
# ============================================================

SUPPORTED_EXTENSIONS = {

    ".txt",

    ".pdf",

    ".docx",

}


# ============================================================
# UPLOAD AND INGEST DOCUMENT
# ============================================================

@router.post(
    "/ingest"
)
async def ingest_document(

    file: UploadFile = File(...),

    current_user: dict = Depends(

        get_current_user

    ),

):

    """
    Upload and ingest a document.

    Authentication required.

    The logged-in user is automatically
    identified using the JWT token.

    Supported formats:
    - TXT
    - PDF
    - DOCX
    """


    # ========================================================
    # VALIDATE CURRENT USER
    # ========================================================

    if not current_user:

        raise HTTPException(

            status_code=401,

            detail=(

                "Authentication required."

            ),

        )


    # ========================================================
    # GET LOGGED-IN USER ID
    # ========================================================

    user_id = current_user.get(

        "user_id"

    )


    # ========================================================
    # GET LOGGED-IN USER EMAIL
    # ========================================================

    user_email = current_user.get(

        "email"

    )


    # ========================================================
    # VALIDATE USER ID
    # ========================================================

    if user_id is None:

        raise HTTPException(

            status_code=401,

            detail=(

                "Authenticated user ID "
                "could not be determined."

            ),

        )


    # ========================================================
    # VALIDATE FILE NAME
    # ========================================================

    if not file.filename:

        raise HTTPException(

            status_code=400,

            detail=(

                "File name is required."

            ),

        )


    # ========================================================
    # GET FILE EXTENSION
    # ========================================================

    extension = (

        Path(

            file.filename

        )

        .suffix

        .lower()

    )


    # ========================================================
    # VALIDATE FILE EXTENSION
    # ========================================================

    if extension not in SUPPORTED_EXTENSIONS:

        raise HTTPException(

            status_code=400,

            detail=(

                "Unsupported file type. "

                "Supported formats: "

                ".txt, .pdf, .docx"

            ),

        )


    # ========================================================
    # CREATE SAFE FILE NAME
    # ========================================================

    safe_filename = (

        Path(

            file.filename

        )

        .name

    )


    # ========================================================
    # CREATE FILE PATH
    # ========================================================

    file_path = (

        DOCUMENT_DIRECTORY

        / safe_filename

    )


    try:

        # ====================================================
        # READ UPLOADED FILE
        # ====================================================

        file_content = (

            await file.read()

        )


        # ====================================================
        # VALIDATE FILE CONTENT
        # ====================================================

        if not file_content:

            raise HTTPException(

                status_code=400,

                detail=(

                    "Uploaded file is empty."

                ),

            )


        # ====================================================
        # SAVE FILE
        # ====================================================

        file_path.write_bytes(

            file_content

        )


        # ====================================================
        # INGEST DOCUMENT
        # ====================================================

        result = (

            ingestion_manager

            .ingest(

                file_path

            )

        )


        # ====================================================
        # RETURN SUCCESS RESPONSE
        # ====================================================

        return {

            "success": True,

            "message": (

                "Document uploaded and "

                "ingested successfully."

            ),

            "user_id": (

                user_id

            ),

            "user_email": (

                user_email

            ),

            "filename": (

                safe_filename

            ),

            "result": (

                result

            ),

        }


    except HTTPException:

        raise


    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=(

                "Document ingestion failed: "

                f"{str(error)}"

            ),

        )


    finally:

        # ====================================================
        # CLOSE UPLOADED FILE
        # ====================================================

        await file.close()


# ============================================================
# INGEST DOCUMENT DIRECTORY
# ============================================================

@router.post(
    "/ingest-directory"
)
def ingest_document_directory(

    current_user: dict = Depends(

        get_current_user

    ),

):

    """
    Ingest all supported documents
    from the default documents directory.

    Authentication required.
    """


    # ========================================================
    # VALIDATE CURRENT USER
    # ========================================================

    if not current_user:

        raise HTTPException(

            status_code=401,

            detail=(

                "Authentication required."

            ),

        )


    # ========================================================
    # GET LOGGED-IN USER ID
    # ========================================================

    user_id = current_user.get(

        "user_id"

    )


    # ========================================================
    # GET LOGGED-IN USER EMAIL
    # ========================================================

    user_email = current_user.get(

        "email"

    )


    # ========================================================
    # VALIDATE USER ID
    # ========================================================

    if user_id is None:

        raise HTTPException(

            status_code=401,

            detail=(

                "Authenticated user ID "
                "could not be determined."

            ),

        )


    try:

        # ====================================================
        # INGEST DOCUMENT DIRECTORY
        # ====================================================

        results = (

            ingestion_manager

            .ingest_directory(

                DOCUMENT_DIRECTORY

            )

        )


        # ====================================================
        # COUNT SUCCESSFUL DOCUMENTS
        # ====================================================

        successful = sum(

            1

            for result in results

            if result.get(

                "status"

            ) == "processed"

        )


        # ====================================================
        # COUNT FAILED DOCUMENTS
        # ====================================================

        failed = sum(

            1

            for result in results

            if result.get(

                "status"

            ) == "failed"

        )


        # ====================================================
        # RETURN RESPONSE
        # ====================================================

        return {

            "success": True,

            "message": (

                "Document directory "

                "ingested successfully."

            ),

            "user_id": (

                user_id

            ),

            "user_email": (

                user_email

            ),

            "directory": str(

                DOCUMENT_DIRECTORY

            ),

            "total_files": (

                len(

                    results

                )

            ),

            "successful": (

                successful

            ),

            "failed": (

                failed

            ),

            "results": (

                results

            ),

        }


    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=(

                "Directory ingestion failed: "

                f"{str(error)}"

            ),

        )


# ============================================================
# GET SUPPORTED EXTENSIONS
# ============================================================

@router.get(
    "/supported-formats"
)
def get_supported_formats():

    """
    Return supported document formats.

    This endpoint is public.
    """

    return {

        "success": True,

        "supported_extensions": (

            sorted(

                SUPPORTED_EXTENSIONS

            )

        ),

    }