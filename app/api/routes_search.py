from fastapi import (
    APIRouter,
    HTTPException
)

from pydantic import BaseModel

from app.services.document_search_service import (
    DocumentSearchService
)


# ========================================================
# API ROUTER
# ========================================================

router = APIRouter(
    prefix="/api/search",
    tags=["Search"]
)


# ========================================================
# SEARCH SERVICE
# ========================================================

search_service = DocumentSearchService(
    top_k=5
)


# ========================================================
# REQUEST MODEL
# ========================================================

class SearchRequest(BaseModel):
    """
    Request model for semantic document search.
    """

    query: str

    top_k: int = 5


# ========================================================
# SEARCH DOCUMENTS
# ========================================================

@router.post("")
def search_documents(
    request: SearchRequest
):
    """
    Perform semantic search across
    indexed document chunks.
    """

    # ====================================================
    # VALIDATE QUERY
    # ====================================================

    query = request.query.strip()

    if not query:

        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty."
        )


    # ====================================================
    # VALIDATE TOP K
    # ====================================================

    if request.top_k <= 0:

        raise HTTPException(
            status_code=400,
            detail="top_k must be greater than zero."
        )


    try:

        # =================================================
        # PERFORM SEMANTIC SEARCH
        # =================================================

        results = search_service.search(
            query=query,
            top_k=request.top_k
        )


        # =================================================
        # RETURN SEARCH RESPONSE
        # =================================================

        return {

            "success": True,

            "query": query,

            "result_count": len(
                results
            ),

            "results": results

        }


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to perform document search. "
                f"Error: {str(error)}"
            )
        )


# ========================================================
# GET SEARCH SERVICE STATUS
# ========================================================

@router.get("/status")
def search_status():
    """
    Return vector search service status.
    """

    try:

        status = search_service.get_status()


        return {

            "success": True,

            "service": (
                "Document Search Service"
            ),

            **status

        }


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ========================================================
# GET TOTAL INDEXED CHUNKS
# ========================================================

@router.get("/count")
def get_indexed_chunk_count():
    """
    Return total number of indexed
    document chunks.
    """

    try:

        total_chunks = (
            search_service
            .get_total_chunks()
        )


        return {

            "success": True,

            "total_chunks": total_chunks

        }


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ========================================================
# GET COLLECTION NAME
# ========================================================

@router.get("/collection")
def get_collection_name():
    """
    Return active ChromaDB collection name.
    """

    try:

        collection_name = (
            search_service
            .get_collection_name()
        )


        return {

            "success": True,

            "collection_name": (
                collection_name
            )

        }


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ========================================================
# SEARCH DOCUMENT BY DOCUMENT ID
# ========================================================

@router.post(
    "/document/{document_id}"
)
def search_specific_document(
    document_id: str,
    request: SearchRequest
):
    """
    Search inside a specific document.
    """

    # ====================================================
    # VALIDATE DOCUMENT ID
    # ====================================================

    document_id = document_id.strip()

    if not document_id:

        raise HTTPException(
            status_code=400,
            detail="Document ID cannot be empty."
        )


    # ====================================================
    # VALIDATE QUERY
    # ====================================================

    query = request.query.strip()

    if not query:

        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty."
        )


    # ====================================================
    # VALIDATE TOP K
    # ====================================================

    if request.top_k <= 0:

        raise HTTPException(
            status_code=400,
            detail="top_k must be greater than zero."
        )


    try:

        # =================================================
        # SEARCH SPECIFIC DOCUMENT
        # =================================================

        results = (
            search_service
            .search_document(
                query=query,
                document_id=document_id,
                top_k=request.top_k
            )
        )


        # =================================================
        # RETURN RESPONSE
        # =================================================

        return {

            "success": True,

            "document_id": document_id,

            "query": query,

            "result_count": len(
                results
            ),

            "results": results

        }


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to search document. "
                f"Error: {str(error)}"
            )
        )


# ========================================================
# DELETE DOCUMENT VECTORS
# ========================================================

@router.delete(
    "/document/{document_id}"
)
def delete_document(
    document_id: str
):
    """
    Delete all vector chunks
    belonging to a document.
    """

    # ====================================================
    # VALIDATE DOCUMENT ID
    # ====================================================

    document_id = document_id.strip()

    if not document_id:

        raise HTTPException(
            status_code=400,
            detail="Document ID cannot be empty."
        )


    try:

        # =================================================
        # DELETE DOCUMENT VECTORS
        # =================================================

        deleted = (
            search_service
            .delete_document(
                document_id
            )
        )


        # =================================================
        # RETURN RESPONSE
        # =================================================

        return {

            "success": True,

            "document_id": document_id,

            "deleted": deleted,

            "message": (
                "Document vectors deleted successfully."
            )

        }


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to delete document vectors. "
                f"Error: {str(error)}"
            )
        )