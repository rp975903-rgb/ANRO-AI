from typing import Any


from app.rag.retrieval_service import (
    RetrievalService
)

from app.rag.rag_generation_service import (
    RAGGenerationService
)


class RAGPipeline:
    """
    Complete end-to-end Retrieval-Augmented Generation pipeline.

    Pipeline:

    User Question
        ↓
    Document Retrieval
        ↓
    Retrieved Chunks
        ↓
    RAG Context Builder
        ↓
    RAG Prompt Builder
        ↓
    Ollama LLM
        ↓
    Final Answer
    """


    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        retrieval_service: RetrievalService | None = None,
        rag_generation_service: (
            RAGGenerationService | None
        ) = None,
        top_k: int = 5,
    ):
        """
        Initialize the complete RAG pipeline.
        """

        # ====================================================
        # VALIDATE TOP K
        # ====================================================

        if top_k <= 0:

            raise ValueError(

                "top_k must be greater than zero."

            )


        self.top_k = top_k


        # ====================================================
        # RETRIEVAL SERVICE
        # ====================================================

        self.retrieval_service = (

            retrieval_service

            if retrieval_service

            else RetrievalService()

        )


        # ====================================================
        # RAG GENERATION SERVICE
        # ====================================================

        self.rag_generation_service = (

            rag_generation_service

            if rag_generation_service

            else RAGGenerationService()

        )


    # ========================================================
    # RUN COMPLETE RAG PIPELINE
    # ========================================================

    def run(
        self,
        question: str,
        top_k: int | None = None,
    ) -> dict[str, Any]:
        """
        Run complete RAG pipeline.

        Steps:

        1. Validate question
        2. Retrieve relevant documents
        3. Build context
        4. Generate AI answer
        5. Return complete result
        """

        # ====================================================
        # VALIDATE QUESTION
        # ====================================================

        if not question:

            raise ValueError(

                "Question cannot be empty."

            )


        question = (

            question.strip()

        )


        if not question:

            raise ValueError(

                "Question cannot be empty."

            )


        # ====================================================
        # DETERMINE TOP K
        # ====================================================

        search_limit = (

            top_k

            if top_k is not None

            else self.top_k

        )


        if search_limit <= 0:

            raise ValueError(

                "top_k must be greater than zero."

            )


        # ====================================================
        # STEP 1 — RETRIEVE DOCUMENTS
        # ====================================================

        retrieval_results = (

            self.retrieval_service

            .search(

                query=question,

                top_k=search_limit,

            )

        )


        # ====================================================
        # STEP 2 — GENERATE RAG ANSWER
        # ====================================================

        generation_result = (

            self.rag_generation_service

            .generate_answer(

                question=question,

                retrieval_results=(
                    retrieval_results
                ),

            )

        )


        # ====================================================
        # RETURN COMPLETE RESULT
        # ====================================================

        return {

            "success":

                True,


            "question":

                question,


            "answer":

                generation_result.get(

                    "answer",

                    ""

                ),


            "retrieval_results":

                retrieval_results,


            "retrieval_result_count":

                len(

                    retrieval_results

                ),


            "context":

                generation_result.get(

                    "context",

                    ""

                ),


            "context_statistics":

                generation_result.get(

                    "context_statistics",

                    {}

                ),


            "prompt_statistics":

                generation_result.get(

                    "prompt_statistics",

                    {},

                ),

        }


    # ========================================================
    # SIMPLE ASK METHOD
    # ========================================================

    def ask(
        self,
        question: str,
        top_k: int | None = None,
    ) -> str:
        """
        Return only the final AI answer.
        """

        result = (

            self.run(

                question=question,

                top_k=top_k,

            )

        )


        return result.get(

            "answer",

            ""

        )


    # ========================================================
    # PIPELINE STATUS
    # ========================================================

    def get_status(
        self,
    ) -> dict[str, Any]:
        """
        Return complete RAG pipeline status.
        """

        # ====================================================
        # GET RAG GENERATION STATUS
        # ====================================================

        generation_status = (

            self.rag_generation_service

            .get_status()

        )


        # ====================================================
        # RETURN STATUS
        # ====================================================

        return {

            "service":

                "RAGPipeline",


            "retrieval_service":

                True,


            "rag_generation_service":

                generation_status,


            "top_k":

                self.top_k,


            "ready":

                (

                    generation_status.get(

                        "ready",

                        False

                    )

                ),

        }