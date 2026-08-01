from typing import Any


from app.ai.embedding_service import (
    EmbeddingService
)

from app.vector_store.chroma_store import (
    ChromaVectorStore
)


class RetrievalService:
    """
    Semantic document retrieval service.

    Complete retrieval pipeline:

    User Query
        ↓
    Query Embedding
        ↓
    ChromaDB Vector Search
        ↓
    Retrieved Document Chunks
        ↓
    Normalized Search Results
    """


    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        vector_store: ChromaVectorStore | None = None,
        embedding_service: EmbeddingService | None = None,
    ):
        """
        Initialize retrieval service.
        """

        # ====================================================
        # VECTOR STORE
        # ====================================================

        self.vector_store = (

            vector_store

            if vector_store is not None

            else ChromaVectorStore()

        )


        # ====================================================
        # EMBEDDING SERVICE
        # ====================================================

        self.embedding_service = (

            embedding_service

            if embedding_service is not None

            else EmbeddingService()

        )


    # ========================================================
    # SEARCH DOCUMENTS
    # ========================================================

    def search(
        self,
        query: str,
        top_k: int = 5,
        document_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search relevant document chunks
        using semantic similarity.
        """

        # ====================================================
        # VALIDATE QUERY
        # ====================================================

        if not query:

            raise ValueError(

                "Search query cannot be empty."

            )


        query = query.strip()


        if not query:

            raise ValueError(

                "Search query cannot be empty."

            )


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


        # ====================================================
        # STEP 1 — GENERATE QUERY EMBEDDING
        # ====================================================

        query_embeddings = (

            self.embedding_service

            .generate_embeddings(

                [query]

            )

        )


        # ====================================================
        # VALIDATE QUERY EMBEDDING
        # ====================================================

        if query_embeddings is None:

            raise ValueError(

                "Query embedding generation failed."

            )


        if len(query_embeddings) == 0:

            raise ValueError(

                "Query embedding generation returned "
                "no embeddings."

            )


        # ====================================================
        # GET SINGLE QUERY EMBEDDING
        # ====================================================

        query_embedding = (

            query_embeddings[0]

        )


        # ====================================================
        # STEP 2 — SEARCH CHROMADB
        # ====================================================

        raw_results = (

            self.vector_store

            .search(

                query_embedding=query_embedding,

                top_k=top_k,

                document_id=document_id,

            )

        )


        # ====================================================
        # STEP 3 — NORMALIZE RESULTS
        # ====================================================

        return self._normalize_results(

            raw_results

        )


    # ========================================================
    # NORMALIZE CHROMADB RESULTS
    # ========================================================

    def _normalize_results(
        self,
        results: dict,
    ) -> list[dict[str, Any]]:
        """
        Convert raw ChromaDB response
        into clean retrieval result objects.
        """

        if not results:

            return []


        ids = results.get(

            "ids",

            [[]]

        )


        documents = results.get(

            "documents",

            [[]]

        )


        metadatas = results.get(

            "metadatas",

            [[]]

        )


        distances = results.get(

            "distances",

            [[]]

        )


        # ====================================================
        # SAFELY GET FIRST QUERY RESULTS
        # ====================================================

        ids = (

            ids[0]

            if ids

            else []

        )


        documents = (

            documents[0]

            if documents

            else []

        )


        metadatas = (

            metadatas[0]

            if metadatas

            else []

        )


        distances = (

            distances[0]

            if distances

            else []

        )


        # ====================================================
        # BUILD NORMALIZED RESULTS
        # ====================================================

        normalized_results = []


        for index, vector_id in enumerate(

            ids

        ):

            text = (

                documents[index]

                if index < len(

                    documents

                )

                else ""

            )


            metadata = (

                metadatas[index]

                if index < len(

                    metadatas

                )

                else {}

            )


            distance = (

                distances[index]

                if index < len(

                    distances

                )

                else None

            )


            normalized_results.append(

                {

                    "rank":

                        index + 1,


                    "vector_id":

                        vector_id,


                    "text":

                        text,


                    "metadata":

                        metadata,


                    "distance":

                        distance,

                }

            )


        return normalized_results


    # ========================================================
    # GET RESULT COUNT
    # ========================================================

    def get_result_count(
        self,
        query: str,
        top_k: int = 5,
        document_id: str | None = None,
    ) -> int:
        """
        Return number of retrieved results.
        """

        results = self.search(

            query=query,

            top_k=top_k,

            document_id=document_id,

        )


        return len(

            results

        )


    # ========================================================
    # RETRIEVAL STATUS
    # ========================================================

    def get_status(
        self,
    ) -> dict[str, Any]:
        """
        Return retrieval service status.
        """

        vector_store_ready = (

            self.vector_store

            is not None

        )


        embedding_service_ready = (

            self.embedding_service

            is not None

        )


        return {

            "service":

                "RetrievalService",


            "vector_store":

                "ChromaVectorStore",


            "embedding_service":

                "EmbeddingService",


            "vector_store_ready":

                vector_store_ready,


            "embedding_service_ready":

                embedding_service_ready,


            "ready":

                (

                    vector_store_ready

                    and

                    embedding_service_ready

                ),

        }