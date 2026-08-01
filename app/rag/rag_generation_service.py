from typing import Any


from app.rag.rag_context_builder import (
    RAGContextBuilder
)

from app.rag.rag_prompt_builder import (
    RAGPromptBuilder
)

from app.ai.ollama_service import (
    OllamaService
)


class RAGGenerationService:
    """
    Complete RAG generation service.

    Pipeline:

    Retrieval Results
        ↓
    RAG Context Builder
        ↓
    RAG Prompt Builder
        ↓
    Ollama LLM
        ↓
    Final AI Answer
    """


    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        max_context_length: int = 5000,
        ollama_service: OllamaService | None = None,
    ):
        """
        Initialize RAG generation components.
        """

        # ====================================================
        # CONTEXT BUILDER
        # ====================================================

        self.context_builder = (

            RAGContextBuilder(

                max_context_length=(
                    max_context_length
                )

            )

        )


        # ====================================================
        # PROMPT BUILDER
        # ====================================================

        self.prompt_builder = (

            RAGPromptBuilder()

        )


        # ====================================================
        # OLLAMA SERVICE
        # ====================================================

        self.ollama_service = (

            ollama_service

            if ollama_service

            else OllamaService()

        )


    # ========================================================
    # GENERATE RAG ANSWER
    # ========================================================

    def generate_answer(
        self,
        question: str,
        retrieval_results: list[dict],
    ) -> dict[str, Any]:
        """
        Generate an AI answer using
        retrieved document context.
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


        # ====================================================
        # VALIDATE RETRIEVAL RESULTS
        # ====================================================

        if retrieval_results is None:

            retrieval_results = []


        # ====================================================
        # BUILD RAG CONTEXT
        # ====================================================

        context = (

            self.context_builder

            .build_context(

                retrieval_results

            )

        )


        # ====================================================
        # BUILD RAG PROMPT
        # ====================================================

        prompts = (

            self.prompt_builder

            .build_prompt(

                question,

                context

            )

        )


        # ====================================================
        # GET SYSTEM PROMPT
        # ====================================================

        system_prompt = (

            prompts.get(

                "system_prompt",

                ""

            )

        )


        # ====================================================
        # GET USER PROMPT
        # ========================================================

        user_prompt = (

            prompts.get(

                "user_prompt",

                ""

            )

        )


        # ====================================================
        # VALIDATE PROMPTS
        # ====================================================

        if not system_prompt:

            raise ValueError(

                "RAG system prompt was not generated."

            )


        if not user_prompt:

            raise ValueError(

                "RAG user prompt was not generated."

            )


        # ====================================================
        # GENERATE AI RESPONSE
        # ====================================================

        answer = (

            self.ollama_service

            .generate_rag_response(

                system_prompt=(
                    system_prompt
                ),

                user_prompt=(
                    user_prompt
                ),

            )

        )


        # ====================================================
        # GET CONTEXT STATISTICS
        # ====================================================

        context_statistics = (

            self.context_builder

            .get_context_statistics(

                context

            )

        )


        # ====================================================
        # GET PROMPT STATISTICS
        # ====================================================

        prompt_statistics = (

            self.prompt_builder

            .get_prompt_statistics(

                question,

                context

            )

        )


        # ====================================================
        # RETURN RESULT
        # ====================================================

        return {

            "success":

                True,


            "question":

                question,


            "answer":

                answer,


            "context":

                context,


            "context_statistics":

                context_statistics,


            "prompt_statistics":

                prompt_statistics,


            "retrieval_result_count":

                len(

                    retrieval_results

                ),

        }


    # ========================================================
    # SIMPLE ANSWER METHOD
    # ========================================================

    def ask(
        self,
        question: str,
        retrieval_results: list[dict],
    ) -> str:
        """
        Generate only the final AI answer.
        """

        result = (

            self.generate_answer(

                question,

                retrieval_results

            )

        )


        return result[

            "answer"

        ]


    # ========================================================
    # SERVICE STATUS
    # ========================================================

    def get_status(
        self,
    ) -> dict[str, Any]:
        """
        Return RAG generation service status.
        """

        ollama_status = (

            self.ollama_service

            .get_status()

        )


        return {

            "service":

                "RAGGenerationService",


            "context_builder":

                True,


            "prompt_builder":

                True,


            "ollama":

                ollama_status,


            "ready":

                (

                    ollama_status.get(

                        "ready",

                        False

                    )

                ),

        }