from pathlib import Path

from app.document_processing.document_ingestion_service import (
    DocumentIngestionService,
)

from app.rag.chunking.text_chunker import (
    TextChunker,
)

from app.storage.json_storage import (
    JSONStorage,
)

from app.database.metadata_database import (
    MetadataDatabase,
)

class DocumentProcessor:
    """
    Complete document processing pipeline.

    Pipeline:

    File
    ↓
    Ingestion
    ↓
    Text Cleaning
    ↓
    Chunking
    ↓
    Persistence
    """


    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ):

        self.ingestion_service = (

            DocumentIngestionService()

        )
        self.database = MetadataDatabase()




        self.chunker = TextChunker(

            chunk_size=chunk_size,

            chunk_overlap=chunk_overlap

        )


        self.storage = JSONStorage()


    def process(
        self,
        file_path: str | Path
    ) -> dict:
        """
        Process a document through
        the complete pipeline.
        """

        # ==================================================
        # STEP 1 — INGEST DOCUMENT
        # ==================================================

        ingestion_result = (

            self.ingestion_service

            .ingest(

                file_path

            )

        )


        document = (

            ingestion_result["document"]

        )


        clean_text = (

            ingestion_result["text"]

        )


        # ==================================================
        # STEP 2 — CREATE CHUNKS
        # ==================================================

        chunks = (

            self.chunker

            .create_chunks(

                text=clean_text,

                document_id=(
                    document.document_id
                )

            )

        )


        # ==================================================
        # STEP 3 — UPDATE DOCUMENT
        # ==================================================

        document.total_chunks = (

            len(chunks)

        )


        document.status = (

            document.status

        )


        # ==================================================
        # STEP 4 — CONVERT CHUNKS
        # ==================================================

        chunk_data = [

            chunk.to_dict()

            for chunk in chunks

        ]


        # ==================================================
        # STEP 5 — SAVE DATA
        # ==================================================

        storage_path = (

            self.storage

            .save_document(

                document=(
                    document.to_dict()
                ),

                chunks=chunk_data

            )

        )


        # ==================================================
        # STEP 6 — RETURN RESULT
        # ==================================================

        # ==================================================
        # STEP 7 — UPDATE DATABASE
        # ==================================================
        self.database.add_document(

    document_id=document.document_id,

    filename=document.filename,

    file_type=document.file_type,

    file_path=document.file_path,

    storage_path=str(
        storage_path
    ),

    total_chunks=len(chunks),

    status=document.status.value

)