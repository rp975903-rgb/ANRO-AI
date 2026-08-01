from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class DatasetStatus(Enum):
    """
    Possible dataset processing states.
    """

    PENDING = "pending"

    LOADED = "loaded"

    PROCESSING = "processing"

    PROCESSED = "processed"

    FAILED = "failed"


@dataclass
class Dataset:
    """
    Represents a structured dataset
    inside NEXUS AI.
    """

    filename: str

    file_type: str

    file_path: str

    dataset_id: str = field(
        default_factory=lambda:
            str(uuid4())
    )

    rows_count: int = 0

    columns_count: int = 0

    status: DatasetStatus = (
        DatasetStatus.PENDING
    )

    created_at: datetime = field(
        default_factory=datetime.now
    )


    def validate(self) -> None:
        """
        Validate dataset information.
        """

        if not self.filename.strip():

            raise ValueError(
                "Dataset filename cannot be empty."
            )


        if not self.file_type.strip():

            raise ValueError(
                "Dataset file type cannot be empty."
            )


        if not self.file_path.strip():

            raise ValueError(
                "Dataset file path cannot be empty."
            )


        if self.rows_count < 0:

            raise ValueError(
                "Rows count cannot be negative."
            )


        if self.columns_count < 0:

            raise ValueError(
                "Columns count cannot be negative."
            )


    def to_dict(self) -> dict:
        """
        Convert dataset object into dictionary.
        """

        return {

            "dataset_id":
                self.dataset_id,

            "filename":
                self.filename,

            "file_type":
                self.file_type,

            "file_path":
                self.file_path,

            "rows_count":
                self.rows_count,

            "columns_count":
                self.columns_count,

            "status":
                self.status.value,

            "created_at":
                self.created_at.isoformat(),

        }