from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4

class DocumentStatus(Enum):
    """Represents document processing status."""

    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


@dataclass
class Document:
    """Represents a document inside ANRO AI.

    Each document belongs to an authenticated user.
    """

    filename: str
    file_type: str
    file_path: str

    # ========================================================
    # DOCUMENT OWNER
    # ========================================================
    user_id: int = 0

    # ========================================================
    # DOCUMENT STATUS
    # ========================================================
    status: DocumentStatus = DocumentStatus.PENDING

    # ========================================================
    # DOCUMENT ID
    # ========================================================
    document_id: str = field(default_factory=lambda: str(uuid4()))

    # ========================================================
    # CREATION TIME
    # ========================================================
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds")
    )

    # ========================================================
    # TOTAL CHUNKS
    # ========================================================
    total_chunks: int = 0

    # ========================================================
    # VALIDATE DOCUMENT
    # ========================================================
    def validate(self):
        """Validate document information."""

        if not self.filename:
            raise ValueError("Document filename cannot be empty.")

        if not self.file_type:
            raise ValueError("Document file type cannot be empty.")

        if not self.file_path:
            raise ValueError("Document file path cannot be empty.")

        if self.user_id <= 0:
            raise ValueError("Document must belong to a valid user.")

    # ========================================================
    # CONVERT DOCUMENT TO DICTIONARY
    # ========================================================
    def to_dict(self) -> dict:
        """Convert document into dictionary."""

        return {
            "document_id": self.document_id,
            "user_id": self.user_id,
            "filename": self.filename,
            "file_type": self.file_type,
            "file_path": self.file_path,
            "status": self.status.value,
            "created_at": self.created_at,
            "total_chunks": self.total_chunks,
        }

