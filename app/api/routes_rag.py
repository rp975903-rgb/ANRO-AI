from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from pydantic import (
    BaseModel,
)

from app.auth.dependencies import (
    get_current_user,
)

from app.rag.rag_pipeline import (
    RAGPipeline,
)


# ============================================================
# RAG API ROUTER
# ============================================================

router = APIRouter(
    prefix="/api/rag",
    tags=["RAG"],
)


# ============================================================
# RAG PIPELINE
# ============================================================

rag_pipeline = RAGPipeline(
    top_k=5
)


# ============================================================
# REQUEST MODEL
# ============================================================

class RAGRequest(BaseModel):

    question: str

    document_id: str | None = None


# ============================================================
# ASK RAG QUESTION
# ============================================================

@router.post(
    "/ask"
)
def ask_question(

    request: RAGRequest,

    current_user=Depends(
        get_current_user
    ),

):

    # ========================================================
    # VALIDATE QUESTION
    # ========================================================

    question = (
        request.question
        or ""
    ).strip()


    if not question:

        raise HTTPException(

            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),

            detail=(
                "Question cannot be empty."
            ),

        )


    # ========================================================
    # EXECUTE RAG PIPELINE
    # ========================================================

    try:

        result = (

            rag_pipeline

            .run(

                question=question,

                top_k=5,

            )

        )


        # ====================================================
        # RETURN RAG RESPONSE
        # ====================================================

        return {

            "success": True,

            "user_id": current_user.get(
                "user_id"
            ),

            "question": question,

            "document_id": request.document_id,

            "answer": result.get(
                "answer",
                ""
            ),

            "retrieval_result_count": result.get(
                "retrieval_result_count",
                0
            ),

            "retrieved_results": result.get(
                "retrieval_results",
                []
            ),

            "context_statistics": result.get(
                "context_statistics",
                {}
            ),

            "prompt_statistics": result.get(
                "prompt_statistics",
                {}
            ),

        }


    # ========================================================
    # HANDLE VALIDATION ERROR
    # ========================================================

    except ValueError as error:

        raise HTTPException(

            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),

            detail=str(
                error
            ),

        )


    # ========================================================
    # HANDLE SERVER ERROR
    # ========================================================

    except Exception as error:

        raise HTTPException(

            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),

            detail=(
                "Failed to generate RAG response. "
                f"Error: {str(error)}"
            ),

        )


# ============================================================
# RAG STATUS
# ============================================================

@router.get(
    "/status"
)
def rag_status(

    current_user=Depends(
        get_current_user
    ),

):

    try:

        pipeline_status = (

            rag_pipeline

            .get_status()

        )


        return {

            "success": True,

            "user_id": current_user.get(
                "user_id"
            ),

            "service": (
                "ANRO AI RAG Pipeline"
            ),

            "status": (

                "ready"

                if pipeline_status.get(
                    "ready",
                    False
                )

                else "not_ready"

            ),

            "pipeline": pipeline_status,

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


# ============================================================
# GET CONVERSATION
# ============================================================

@router.get(
    "/conversation"
)
def get_conversation(

    current_user=Depends(
        get_current_user
    ),

):

    return {

        "success": True,

        "user_id": current_user.get(
            "user_id"
        ),

        "message": (

            "Conversation memory is currently "

            "managed by the RAG generation service."

        ),

    }


# ============================================================
# CLEAR CONVERSATION
# ============================================================

@router.delete(
    "/conversation"
)
def clear_conversation(

    current_user=Depends(
        get_current_user
    ),

):

    return {

        "success": True,

        "user_id": current_user.get(
            "user_id"
        ),

        "message": (

            "Conversation clear endpoint is "

            "available. Persistent conversation "

            "memory implementation can be added "

            "in the next stage."

        ),

    }