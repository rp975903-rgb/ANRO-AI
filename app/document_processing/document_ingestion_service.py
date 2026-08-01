from pathlib import Path
from uuid import uuid4

from app.ai.embedding_service import (
    EmbeddingService
)

from app.database.metadata_database import (
    MetadataDatabase
)

from app.vector_store.chroma_store import (
    ChromaVectorStore
)

from app.document_processing.document_loader_factory import (
    DocumentLoaderFactory
)

from app.nlp.text_cleaner import (
    TextCleaner
)

from app.rag.chunking.text_chunker import (
    TextChunker
)


class DocumentIngestionService:
    """
    Professional document ingestion pipeline.

    Pipeline:

    Document
        ↓
    Document Loader Factory
        ↓
    Text Extraction
        ↓
    Text Cleaning
        ↓
    Text Chunking
        ↓
    Embedding Generation
        ↓
    ChromaDB Vector Storage
        ↓
    SQLite Metadata Storage
    """

    def __init__(self):

        # ====================================================
        # AI EMBEDDING SERVICE
        # ====================================================

        self.embedding_service = (
            EmbeddingService()
        )


        # ====================================================
        # VECTOR DATABASE
        # ====================================================

        self.vector_store = (
            ChromaVectorStore()
        )


        # ====================================================
        # METADATA DATABASE
        # ====================================================

        self.database = (
            MetadataDatabase()
        )


        # ====================================================
        # TEXT CLEANER
        # ====================================================

        self.text_cleaner = (
            TextCleaner()
        )


        # ====================================================
        # TEXT CHUNKER
        # ====================================================

        self.text_chunker = (

            TextChunker(

                chunk_size=500,

                chunk_overlap=50

            )

        )


    # ========================================================
    # INGEST DOCUMENT
    # ========================================================

    def ingest_document(

        self,

        file_path: str | Path

    ):

        # ====================================================
        # STEP 1 — VALIDATE FILE PATH
        # ====================================================

        file_path = Path(

            file_path

        )


        if not file_path.exists():

            raise FileNotFoundError(

                f"Document not found: "
                f"{file_path}"

            )


        if not file_path.is_file():

            raise ValueError(

                "Provided path is not a file."

            )


        # ====================================================
        # STEP 2 — GENERATE DOCUMENT ID
        # ====================================================

        document_id = str(

            uuid4()

        )


        # ====================================================
        # STEP 3 — SELECT DOCUMENT LOADER
        # ====================================================

        loader = (

            DocumentLoaderFactory

            .get_loader(

                file_path

            )

        )


        # ====================================================
        # STEP 4 — EXTRACT TEXT
        # ====================================================

        raw_text = (

            loader

            .load(

                file_path

            )

        )


        if not raw_text.strip():

            raise ValueError(

                "Cannot ingest an empty document."

            )


        # ====================================================
        # STEP 5 — CLEAN TEXT
        # ====================================================

        cleaned_text = (

            self.text_cleaner

            .clean(

                raw_text

            )

        )


        if not cleaned_text.strip():

            raise ValueError(

                "Document contains no usable text "
                "after cleaning."

            )


        # ====================================================
        # STEP 6 — CREATE TEXT CHUNKS
        # ====================================================

        chunks = (

            self.text_chunker

            .create_chunks(

                text=cleaned_text,

                document_id=document_id

            )

        )


        if not chunks:

            raise ValueError(

                "No chunks were created."

            )


        # ====================================================
        # STEP 7 — EXTRACT CHUNK TEXT
        # ====================================================

        chunk_texts = [

            chunk.text

            for chunk in chunks

        ]


        # ====================================================
        # STEP 8 — GENERATE EMBEDDINGS
        # ====================================================

        embeddings = (

            self.embedding_service

            .generate_embeddings(

                chunk_texts

            )

        )


        # ====================================================
        # STEP 9 — STORE VECTORS
        # ====================================================

        vector_ids = (

            self.vector_store

            .add_chunks(

                document_id,

                chunks,

                embeddings

            )

        )


        # ====================================================
        # STEP 10 — SAVE DOCUMENT METADATA
        # ====================================================

        self.database.add_document(

            document_id=document_id,

            filename=file_path.name,

            file_type=file_path.suffix.lower(),

            file_path=str(file_path),

            storage_path=str(file_path),

            total_chunks=len(chunks),

            status="processed"

        )


        # ====================================================
        # STEP 11 — RETURN INGESTION RESULT
        # ====================================================

        return {

            "document_id":
                document_id,

            "filename":
                file_path.name,

            "file_type":
                file_path.suffix.lower(),

            "total_chunks":
                len(chunks),

            "vector_ids":
                vector_ids,

            "status":
                "processed"

        }