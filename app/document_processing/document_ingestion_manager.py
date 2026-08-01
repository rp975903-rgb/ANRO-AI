from pathlib import Path

from uuid import uuid4


from app.document_processing.txt_loader import (
    TXTLoader
)

from app.document_processing.pdf_loader import (
    PDFLoader
)

from app.document_processing.docx_loader import (
    DOCXLoader
)

from app.nlp.text_cleaner import (
    TextCleaner
)

from app.rag.chunking.text_chunker import (
    TextChunker
)

from app.ai.embedding_service import (
    EmbeddingService
)

from app.vector_store.chroma_store import (
    ChromaVectorStore
)

from app.database.metadata_database import (
    MetadataDatabase
)


class DocumentIngestionManager:
    """
    Complete document ingestion pipeline.

    Pipeline:

    Document
        ↓
    File Validation
        ↓
    Document Loader
        ↓
    Text Extraction
        ↓
    Text Cleaning
        ↓
    Text Chunking
        ↓
    Embedding Generation
        ↓
    ChromaDB Storage
        ↓
    Metadata Database
        ↓
    User Ownership
    """


    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(

        self,

        chunk_size: int = 500,

        chunk_overlap: int = 50

    ):

        # ====================================================
        # DOCUMENT LOADERS
        # ====================================================

        self.loaders = {

            ".txt": TXTLoader(),

            ".pdf": PDFLoader(),

            ".docx": DOCXLoader(),

        }


        # ====================================================
        # TEXT CLEANER
        # ====================================================

        self.text_cleaner = TextCleaner()


        # ====================================================
        # TEXT CHUNKER
        # ====================================================

        self.text_chunker = TextChunker(

            chunk_size=chunk_size,

            chunk_overlap=chunk_overlap

        )


        # ====================================================
        # EMBEDDING SERVICE
        # ====================================================

        self.embedding_service = EmbeddingService()


        # ====================================================
        # VECTOR STORE
        # ====================================================

        self.vector_store = ChromaVectorStore(

            persist_directory="data/vector_db"

        )


        # ====================================================
        # METADATA DATABASE
        # ====================================================

        self.database = MetadataDatabase()


    # ========================================================
    # GET SUPPORTED EXTENSIONS
    # ========================================================

    def get_supported_extensions(

        self

    ) -> list[str]:

        """
        Return supported document extensions.
        """

        return sorted(

            self.loaders.keys()

        )


    # ========================================================
    # GET DOCUMENT LOADER
    # ========================================================

    def get_loader(

        self,

        path: Path

    ):

        """
        Return the correct loader
        according to file extension.
        """

        extension = (

            path.suffix.lower()

        )


        if extension not in self.loaders:

            raise ValueError(

                f"Unsupported file type: "

                f"{extension}. "

                f"Supported extensions: "

                f"{self.get_supported_extensions()}"

            )


        return self.loaders[extension]


    # ========================================================
    # INGEST SINGLE DOCUMENT
    # ========================================================

    def ingest(

        self,

        file_path: str | Path,

        user_id: int | None = None

    ) -> dict:

        """
        Process and index a single document.

        The document is automatically associated
        with the authenticated user ID.
        """


        # ====================================================
        # STEP 1 — CONVERT PATH
        # ====================================================

        path = Path(

            file_path

        )


        # ====================================================
        # STEP 2 — CHECK FILE EXISTS
        # ====================================================

        if not path.exists():

            raise FileNotFoundError(

                f"Document not found: {path}"

            )


        # ====================================================
        # STEP 3 — CHECK IS FILE
        # ====================================================

        if not path.is_file():

            raise ValueError(

                f"Provided path is not a file: {path}"

            )


        # ====================================================
        # STEP 4 — GET EXTENSION
        # ====================================================

        extension = (

            path.suffix.lower()

        )


        # ====================================================
        # STEP 5 — VALIDATE EXTENSION
        # ====================================================

        if extension not in self.loaders:

            raise ValueError(

                f"Unsupported file type: "

                f"{extension}. "

                f"Supported extensions: "

                f"{self.get_supported_extensions()}"

            )


        # ====================================================
        # STEP 6 — GENERATE DOCUMENT ID
        # ====================================================

        document_id = str(

            uuid4()

        )


        # ====================================================
        # STEP 7 — GET LOADER
        # ====================================================

        loader = self.get_loader(

            path

        )


        # ====================================================
        # STEP 8 — EXTRACT TEXT
        # ====================================================

        raw_text = loader.load(

            path

        )


        if not isinstance(

            raw_text,

            str

        ):

            raise TypeError(

                "Document loader must "

                "return text as a string."

            )


        if not raw_text.strip():

            raise ValueError(

                "Document does not contain "

                "extractable text."

            )


        # ====================================================
        # STEP 9 — CLEAN TEXT
        # ====================================================

        cleaned_text = (

            self.text_cleaner

            .clean(

                raw_text

            )

        )


        if not cleaned_text:

            raise ValueError(

                "Document became empty "

                "after text cleaning."

            )


        # ====================================================
        # STEP 10 — CREATE CHUNKS
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

                "No text chunks were created."

            )


        # ====================================================
        # STEP 11 — EXTRACT CHUNK TEXT
        # ====================================================

        chunk_texts = [

            chunk.text

            for chunk in chunks

        ]


        if not chunk_texts:

            raise ValueError(

                "No chunk text was generated."

            )


        # ====================================================
        # STEP 12 — GENERATE EMBEDDINGS
        # ====================================================

        embeddings = (

            self.embedding_service

            .generate_embeddings(

                chunk_texts

            )

        )


        if embeddings is None:

            raise ValueError(

                "No embeddings were generated."

            )


        if len(embeddings) == 0:

            raise ValueError(

                "No embeddings were generated."

            )


        # ====================================================
        # STEP 13 — VALIDATE COUNTS
        # ====================================================

        if len(chunks) != len(embeddings):

            raise ValueError(

                "Number of chunks and embeddings "

                "must be equal."

            )


        # ====================================================
        # STEP 14 — STORE IN CHROMADB
        # ====================================================

        vector_ids = (

            self.vector_store

            .add_chunks(

                document_id=document_id,

                chunks=chunks,

                embeddings=embeddings

            )

        )


        # ====================================================
        # STEP 15 — SAVE METADATA
        # ====================================================

        self.database.add_document(

            document_id=document_id,

            filename=path.name,

            file_type=extension,

            file_path=str(path),

            storage_path=str(path),

            total_chunks=len(chunks),

            status="processed",

            user_id=user_id

        )


        # ====================================================
        # STEP 16 — RETURN RESULT
        # ====================================================

        return {

            "document_id":

                document_id,

            "user_id":

                user_id,

            "filename":

                path.name,

            "file_type":

                extension,

            "file_path":

                str(path),

            "characters":

                len(cleaned_text),

            "total_chunks":

                len(chunks),

            "vector_ids":

                vector_ids,

            "status":

                "processed",

        }


    # ========================================================
    # INGEST DIRECTORY
    # ========================================================

    def ingest_directory(

        self,

        directory_path: str | Path,

        user_id: int | None = None

    ) -> list[dict]:

        """
        Process all supported documents
        inside a directory.

        All documents are associated
        with the authenticated user.
        """


        # ====================================================
        # STEP 1 — CONVERT PATH
        # ====================================================

        directory = Path(

            directory_path

        )


        # ====================================================
        # STEP 2 — VALIDATE DIRECTORY
        # ====================================================

        if not directory.exists():

            raise FileNotFoundError(

                f"Directory not found: "

                f"{directory}"

            )


        if not directory.is_dir():

            raise ValueError(

                f"Provided path is not a directory: "

                f"{directory}"

            )


        # ====================================================
        # STEP 3 — FIND SUPPORTED FILES
        # ====================================================

        files = [

            file

            for file in directory.iterdir()

            if (

                file.is_file()

                and

                file.suffix.lower()

                in self.loaders

            )

        ]


        # ====================================================
        # STEP 4 — SORT FILES
        # ====================================================

        files.sort(

            key=lambda file:

                file.name.lower()

        )


        # ====================================================
        # STEP 5 — PROCESS FILES
        # ====================================================

        results = []


        for file in files:

            try:

                result = self.ingest(

                    file,

                    user_id=user_id

                )


                results.append(

                    result

                )


            except Exception as error:

                results.append(

                    {

                        "filename":

                            file.name,

                        "file_type":

                            file.suffix.lower(),

                        "user_id":

                            user_id,

                        "status":

                            "failed",

                        "error":

                            str(error),

                    }

                )


        # ====================================================
        # STEP 6 — RETURN RESULTS
        # ====================================================

        return results