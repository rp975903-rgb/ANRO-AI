from pathlib import Path

import chromadb


class ChromaVectorStore:
    """
    Vector database service using ChromaDB.

    Responsibilities:

    - Create persistent ChromaDB storage
    - Create or load collections
    - Add document chunks
    - Search similar chunks
    - Delete document vectors
    - Count stored vectors
    - Get collection information
    """

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        persist_directory: str = "data/vector_db",
        collection_name: str = "ANRO_documents"
    ):
        """
        Initialize persistent ChromaDB vector store.
        """

        # ====================================================
        # VECTOR STORE DIRECTORY
        # ====================================================

        self.persist_directory = Path(
            persist_directory
        )

        self.collection_name = (
            collection_name
        )

        # ====================================================
        # CREATE DIRECTORY
        # ====================================================

        self.persist_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        # ====================================================
        # CREATE CHROMADB CLIENT
        # ====================================================

        self.client = (
            chromadb.PersistentClient(
                path=str(
                    self.persist_directory
                )
            )
        )

        # ====================================================
        # CREATE OR LOAD COLLECTION
        # ====================================================

        self.collection = (
            self.client.get_or_create_collection(
                name=self.collection_name
            )
        )


    # ========================================================
    # ADD DOCUMENT CHUNKS
    # ========================================================

    def add_chunks(
        self,
        document_id: str,
        chunks: list,
        embeddings
    ) -> list[str]:
        """
        Add document chunks and embeddings
        to ChromaDB.
        """

        # ====================================================
        # VALIDATE DOCUMENT ID
        # ====================================================

        if not isinstance(
            document_id,
            str
        ):
            raise TypeError(
                "document_id must be a string."
            )

        if not document_id.strip():
            raise ValueError(
                "document_id cannot be empty."
            )


        # ====================================================
        # VALIDATE CHUNKS
        # ====================================================

        if not chunks:

            raise ValueError(
                "Chunks cannot be empty."
            )


        # ====================================================
        # VALIDATE EMBEDDINGS
        # ====================================================

        if embeddings is None:

            raise ValueError(
                "Embeddings cannot be None."
            )


        if len(embeddings) == 0:

            raise ValueError(
                "Embeddings cannot be empty."
            )


        # ====================================================
        # VALIDATE CHUNK / EMBEDDING COUNT
        # ====================================================

        if len(chunks) != len(embeddings):

            raise ValueError(
                "Chunks and embeddings "
                "must have the same length."
            )


        # ====================================================
        # EXTRACT CHUNK IDS
        # ====================================================

        ids = [

            chunk.chunk_id

            for chunk in chunks

        ]


        # ====================================================
        # EXTRACT DOCUMENT TEXT
        # ====================================================

        documents = [

            chunk.text

            for chunk in chunks

        ]


        # ====================================================
        # CREATE METADATA
        # ====================================================

        metadatas = [

            {

                "document_id":
                    chunk.document_id,

                "chunk_index":
                    chunk.chunk_index,

                "start_position":
                    chunk.start_position,

                "end_position":
                    chunk.end_position,

            }

            for chunk in chunks

        ]


        # ====================================================
        # CONVERT EMBEDDINGS
        # ====================================================

        embedding_list = [

            embedding.tolist()

            if hasattr(
                embedding,
                "tolist"
            )

            else list(
                embedding
            )

            for embedding in embeddings

        ]


        # ====================================================
        # STORE IN CHROMADB
        # ====================================================

        self.collection.add(

            ids=ids,

            documents=documents,

            embeddings=embedding_list,

            metadatas=metadatas

        )


        # ====================================================
        # RETURN VECTOR IDS
        # ====================================================

        return ids


    # ========================================================
    # SEARCH SIMILAR CHUNKS
    # ========================================================

    def search(
        self,
        query_embedding,
        top_k: int = 5,
        document_id: str | None = None
    ):
        """
        Search similar document chunks
        using vector similarity.
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


        # ====================================================
        # VALIDATE DOCUMENT ID
        # ====================================================

        if document_id is not None:

            if not isinstance(
                document_id,
                str
            ):

                raise TypeError(
                    "document_id must be a string."
                )


            document_id = (
                document_id.strip()
            )


            if not document_id:

                raise ValueError(
                    "document_id cannot be empty."
                )


        # ====================================================
        # CHECK COLLECTION COUNT
        # ====================================================

        collection_count = (
            self.collection.count()
        )


        # ====================================================
        # EMPTY COLLECTION
        # ====================================================

        if collection_count == 0:

            return {

                "ids": [[]],

                "documents": [[]],

                "metadatas": [[]],

                "distances": [[]],

            }


        # ====================================================
        # CONVERT QUERY EMBEDDING
        # ====================================================

        if hasattr(
            query_embedding,
            "tolist"
        ):

            query_embedding = (
                query_embedding.tolist()
            )


        # ====================================================
        # BUILD SEARCH PARAMETERS
        # ====================================================

        query_parameters = {

            "query_embeddings": [

                query_embedding

            ],

            "n_results": min(

                top_k,

                collection_count

            )

        }


        # ====================================================
        # DOCUMENT-SPECIFIC FILTER
        # ====================================================

        if document_id is not None:

            query_parameters["where"] = {

                "document_id":
                    document_id

            }


        # ====================================================
        # SEARCH CHROMADB
        # ====================================================

        results = (

            self.collection.query(

                **query_parameters

            )

        )


        # ====================================================
        # RETURN SEARCH RESULTS
        # ====================================================

        return results


    # ========================================================
    # DELETE DOCUMENT VECTORS
    # ========================================================

    def delete_document(
        self,
        document_id: str
    ) -> bool:
        """
        Delete all vectors belonging
        to a specific document.
        """

        # ====================================================
        # VALIDATE DOCUMENT ID
        # ====================================================

        if not isinstance(
            document_id,
            str
        ):

            raise TypeError(
                "document_id must be a string."
            )


        document_id = (
            document_id.strip()
        )


        if not document_id:

            raise ValueError(
                "document_id cannot be empty."
            )


        # ====================================================
        # DELETE VECTORS
        # ====================================================

        self.collection.delete(

            where={

                "document_id":
                    document_id

            }

        )


        return True


    # ========================================================
    # COUNT STORED CHUNKS
    # ========================================================

    def count(
        self
    ) -> int:
        """
        Return total number
        of stored document chunks.
        """

        return (
            self.collection.count()
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
            self.collection_name
        )


    # ========================================================
    # GET PERSIST DIRECTORY
    # ========================================================

    def get_persist_directory(
        self
    ) -> str:
        """
        Return ChromaDB
        persistent storage path.
        """

        return str(
            self.persist_directory
        )


    # ========================================================
    # GET VECTOR STORE STATUS
    # ========================================================

    def get_status(
        self
    ) -> dict:
        """
        Return vector store status.
        """

        return {

            "service":
                "ChromaVectorStore",

            "status":
                "ready",

            "collection_name":
                self.collection_name,

            "persist_directory":
                str(
                    self.persist_directory
                ),

            "total_chunks":
                self.count(),

        }