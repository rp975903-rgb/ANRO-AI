from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class ExecutionStatus(Enum):
    """
    Possible AI execution states.
    """

    STARTED = "started"

    COMPLETED = "completed"

    FAILED = "failed"


@dataclass
class AIExecution:
    """
    Represents one AI system execution.
    """

    user_query: str

    execution_id: str = field(
        default_factory=lambda:
            str(uuid4())
    )

    agent_name: str = "unknown"

    response: str = ""

    status: ExecutionStatus = (
        ExecutionStatus.STARTED
    )

    execution_time: float = 0.0

    created_at: datetime = field(
        default_factory=datetime.now
    )


    def validate(self) -> None:
        """
        Validate AI execution data.
        """

        if not self.user_query.strip():

            raise ValueError(
                "User query cannot be empty."
            )


        if self.execution_time < 0:

            raise ValueError(
                "Execution time cannot be negative."
            )


    def mark_completed(
        self,
        response: str,
        execution_time: float
    ) -> None:
        """
        Mark AI execution as completed.
        """

        self.response = response

        self.execution_time = (
            execution_time
        )

        self.status = (
            ExecutionStatus.COMPLETED
        )


    def mark_failed(
        self,
        error_message: str
    ) -> None:
        """
        Mark AI execution as failed.
        """

        self.response = error_message

        self.status = (
            ExecutionStatus.FAILED
        )


    def to_dict(self) -> dict:
        """
        Convert AI execution into dictionary.
        """

        return {

            "execution_id":
                self.execution_id,

            "user_query":
                self.user_query,

            "agent_name":
                self.agent_name,

            "response":
                self.response,

            "status":
                self.status.value,

            "execution_time":
                self.execution_time,

            "created_at":
                self.created_at.isoformat(),

        }