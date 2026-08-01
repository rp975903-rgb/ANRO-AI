from typing import Any


class RAGContextBuilder:
    """
    Builds clean, structured, and controlled
    context from retrieved document chunks.

    This context is later passed to the RAG
    prompt builder / LLM service.
    """

    def __init__(
        self,
        max_context_length: int = 5000,
    ):
        """
        Initialize RAG context builder.

        Args:
            max_context_length:
                Maximum number of characters allowed
                in the final RAG context.
        """

        if max_context_length <= 0:
            raise ValueError(
                "max_context_length must be greater than zero."
            )

        self.max_context_length = max_context_length

    # ========================================================
    # BUILD CONTEXT
    # ========================================================

    def build_context(
        self,
        retrieval_results: list[dict[str, Any]],
    ) -> str:
        """
        Convert retrieved document chunks into
        a structured RAG context.

        The context contains:
        - Source number
        - Document ID
        - Chunk ID
        - Chunk index
        - Similarity distance
        - Actual document content
        """

        # ----------------------------------------------------
        # VALIDATE INPUT
        # ----------------------------------------------------

        if not retrieval_results:
            return ""

        context_parts: list[str] = []

        current_length = 0

        source_number = 0

        # ====================================================
        # PROCESS RETRIEVED RESULTS
        # ====================================================

        for result in retrieval_results:

            # ------------------------------------------------
            # EXTRACT TEXT
            # ------------------------------------------------

            text = str(
                result.get(
                    "text",
                    "",
                )
            ).strip()

            # Skip empty chunks
            if not text:
                continue

            # ------------------------------------------------
            # EXTRACT METADATA
            # ------------------------------------------------

            metadata = result.get(
                "metadata",
                {},
            )

            if not isinstance(
                metadata,
                dict,
            ):
                metadata = {}

            # ------------------------------------------------
            # DOCUMENT INFORMATION
            # ------------------------------------------------

            document_id = str(
                metadata.get(
                    "document_id",
                    "unknown",
                )
            )

            chunk_id = str(
                metadata.get(
                    "chunk_id",
                    result.get(
                        "vector_id",
                        "unknown",
                    ),
                )
            )

            chunk_index = metadata.get(
                "chunk_index",
                "unknown",
            )

            # ------------------------------------------------
            # RETRIEVAL DISTANCE
            # ------------------------------------------------

            distance = result.get(
                "distance",
                None,
            )

            if distance is None:
                distance_text = "unknown"
            else:
                try:
                    distance_text = f"{float(distance):.6f}"
                except (
                    TypeError,
                    ValueError,
                ):
                    distance_text = str(
                        distance
                    )

            # ------------------------------------------------
            # INCREMENT SOURCE NUMBER
            # ------------------------------------------------

            source_number += 1

            # =================================================
            # BUILD SOURCE BLOCK
            # =================================================

            source_block = (
                f"[Source {source_number}]\n"
                f"Document ID: {document_id}\n"
                f"Chunk ID: {chunk_id}\n"
                f"Chunk Index: {chunk_index}\n"
                f"Retrieval Distance: {distance_text}\n"
                f"Content:\n"
                f"{text}\n"
            )

            source_length = len(
                source_block
            )

            # =================================================
            # CONTEXT LENGTH CONTROL
            # =================================================

            if (
                current_length
                + source_length
                > self.max_context_length
            ):

                # If no source has been added yet,
                # include a truncated version.
                if not context_parts:

                    remaining_length = (
                        self.max_context_length
                        - current_length
                    )

                    if remaining_length > 0:

                        truncated_block = (
                            source_block[
                                :remaining_length
                            ]
                        )

                        context_parts.append(
                            truncated_block
                        )

                break

            # ------------------------------------------------
            # ADD SOURCE
            # ------------------------------------------------

            context_parts.append(
                source_block
            )

            current_length += (
                source_length
            )

        # ====================================================
        # RETURN FINAL CONTEXT
        # ====================================================

        return "\n".join(
            context_parts
        )

    # ========================================================
    # GET CONTEXT STATISTICS
    # ========================================================

    def get_context_statistics(
        self,
        context: str,
    ) -> dict[str, Any]:
        """
        Return statistics about
        the generated RAG context.
        """

        if not context:

            return {
                "characters": 0,
                "words": 0,
                "sources": 0,
                "lines": 0,
            }

        return {
            "characters": len(
                context
            ),
            "words": len(
                context.split()
            ),
            "sources": context.count(
                "[Source "
            ),
            "lines": len(
                context.splitlines()
            ),
        }

    # ========================================================
    # CHECK CONTEXT AVAILABILITY
    # ========================================================

    def has_context(
        self,
        context: str,
    ) -> bool:
        """
        Check whether usable RAG context
        is available.
        """

        if not context:
            return False

        return bool(
            context.strip()
        )

    # ========================================================
    # GET SOURCE COUNT
    # ========================================================

    def get_source_count(
        self,
        context: str,
    ) -> int:
        """
        Return the number of sources
        included in the RAG context.
        """

        if not context:
            return 0

        return context.count(
            "[Source "
        )