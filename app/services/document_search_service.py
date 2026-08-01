from app.rag.retrieval_service import (
    RetrievalService
)

from app.vector_store.chroma_store import (
    ChromaVectorStore
)


class DocumentSearchService:
    """
    Professional document search and management service
    for the NEXUS AI document intelligence system.

    Responsibilities:

    - Search relevant document chunks
    - Return similarity information
    - Retrieve document metadata
    - Delete document vectors
    - Count indexed document chunks
    - Get vector collection information
    """

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        top_k: int = 5
    ):
        """
        Initialize document search service.
        """

        # ====================================================
        # VALIDATE TOP K
        # ====================================================

        if not isinstance(
            top_k,
            int
        ):
            raise TypeError(
                "top_k must be an integer."
            )


        if top_k <= 0:

            raise ValueError(
                "top_k must be greater than zero."
            )


        self.top_k = top_k
        # ====================================================
        # VECTOR STORE
        # ====================================================

        self.vector_store = (
            ChromaVectorStore(
                persist_directory="data/vector_db",
                collection_name="ANRO_documents"
            )
        )

        # ====================================================
        # RETRIEVAL SERVICE
        # ====================================================

        self.retrieval_service = (
            RetrievalService(
                vector_store=self.vector_store
            )
        )


    # ========================================================
    # SEARCH DOCUMENTS
    # ========================================================

    def search(
        self,
        query: str,
        top_k: int | None = None
    ) -> list[dict]:
        """
        Search relevant document chunks
        using semantic similarity.
        """

        # ====================================================
        # VALIDATE QUERY TYPE
        # ====================================================

        if not isinstance(
            query,
            str
        ):

            raise TypeError(
                "Query must be a string."
            )


        # ====================================================
        # CLEAN QUERY
        # ====================================================

        query = query.strip()


        if not query:

            raise ValueError(
                "Query cannot be empty."
            )


        # ====================================================
        # DETERMINE RESULT COUNT
        # ====================================================

        result_count = (

            top_k

            if top_k is not None

            else self.top_k

        )


        # ====================================================
        # VALIDATE RESULT COUNT
        # ====================================================

        if not isinstance(
            result_count,
            int
        ):

            raise TypeError(
                "top_k must be an integer."
            )


        if result_count <= 0:

            raise ValueError(
                "top_k must be greater than zero."
            )


        # ====================================================
        # PERFORM SEMANTIC SEARCH
        # ====================================================

        results = (

            self.retrieval_service

            .search(

                query=query,

                top_k=result_count

            )

        )


        # ====================================================
        # FORMAT SEARCH RESULTS
        # ====================================================

        formatted_results = []


        for index, result in enumerate(

            results,

            start=1

        ):

            formatted_results.append(

                {

                    "rank":
                        index,

                    "vector_id":
                        result.get(
                            "vector_id"
                        ),

                    "text":
                        result.get(
                            "text",
                            ""
                        ),

                    "metadata":
                        result.get(
                            "metadata",
                            {}
                        ),

                    "distance":
                        result.get(
                            "distance"
                        ),

                }

            )


        return formatted_results


    # ========================================================
    # SEARCH BY DOCUMENT
    # ========================================================

    def search_document(
        self,
        query: str,
        document_id: str,
        top_k: int | None = None
    ) -> list[dict]:
        """
        Search relevant chunks from
        a specific document.
        """

        # ====================================================
        # VALIDATE DOCUMENT ID
        # ====================================================

        if not isinstance(
            document_id,
            str
        ):

            raise TypeError(
                "Document ID must be a string."
            )


        # ====================================================
        # CLEAN DOCUMENT ID
        # ====================================================

        document_id = (

            document_id.strip()

        )


        if not document_id:

            raise ValueError(
                "Document ID cannot be empty."
            )


        # ====================================================
        # VALIDATE QUERY
        # ====================================================

        if not isinstance(
            query,
            str
        ):

            raise TypeError(
                "Query must be a string."
            )


        # ====================================================
        # SEARCH WITH DOCUMENT FILTER
        # ====================================================

        results = (

            self.retrieval_service

            .search(

                query=query,

                top_k=(

                    top_k

                    if top_k is not None

                    else self.top_k

                ),

                document_id=document_id

            )

        )


        return results


    # ========================================================
    # DELETE DOCUMENT
    # ========================================================

    def delete_document(
        self,
        document_id: str
    ) -> bool:
        """
        Delete all vector chunks
        belonging to a document.
        """

        # ====================================================
        # VALIDATE DOCUMENT ID
        # ====================================================

        if not isinstance(
            document_id,
            str
        ):

            raise TypeError(
                "Document ID must be a string."
            )


        document_id = (

            document_id.strip()

        )


        if not document_id:

            raise ValueError(
                "Document ID cannot be empty."
            )


        # ====================================================
        # DELETE VECTORS
        # ====================================================

        return (

            self.vector_store

            .delete_document(

                document_id

            )

        )


    # ========================================================
    # GET TOTAL CHUNK COUNT
    # ========================================================

    def get_total_chunks(
        self
    ) -> int:
        """
        Return total number of indexed
        document chunks.
        """

        return (

            self.vector_store

            .count()

        )


    # ========================================================
    # GET COLLECTION NAME
    # ========================================================

    def get_collection_name(
        self
    ) -> str:
        """
        Return active ChromaDB
        collection name.
        """

        return (

            self.vector_store

            .get_collection_name()

        )


    # ========================================================
    # GET SERVICE STATUS
    # ========================================================

    def get_status(
        self
    ) -> dict:
        """
        Return document search service status.
        """

        return {

            "service":
                "DocumentSearchService",

            "status":
                "ready",

            "collection_name":
                self.get_collection_name(),

            "total_chunks":
                self.get_total_chunks(),

            "top_k":
                self.top_k,

            "retrieval_service":
                self.retrieval_service
                .get_status(),

        }