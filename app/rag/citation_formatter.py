class CitationFormatter:
    """
    Formats retrieved document chunks
    into clean source citations.
    """

    def __init__(self, preview_length: int = 200):
        self.preview_length = preview_length

    def format_sources(
        self,
        retrieval_results: list[dict] | None
    ) -> list[dict]:

        if retrieval_results is None:
            return []

        citations = []

        for index, result in enumerate(
            retrieval_results,
            start=1
        ):
            metadata = result.get(
                "metadata",
                {}
            )

            citation = {
                "source_number": index,
                "document_id": metadata.get(
                    "document_id",
                    "unknown"
                ),
                "chunk_index": metadata.get(
                    "chunk_index",
                    "unknown"
                ),
            }

            citations.append(citation)

        return citations