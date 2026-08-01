from app.ai.llm.base_llm import (
    BaseLLM
)


class MockLLM(BaseLLM):
    """
    Mock LLM used for testing
    the NEXUS AI RAG pipeline.

    This class does not call
    any external AI API.
    """


    def __init__(
        self,
        model_name: str = "nexus-mock-llm"
    ):

        self.model_name = model_name


    # ========================================================
    # GENERATE ANSWER
    # ========================================================

    def generate(
        self,
        prompt: str
    ) -> str:

        if not prompt.strip():

            raise ValueError(

                "Prompt cannot be empty."

            )


        return (

            "This is a mock response "
            "generated for testing the "
            "NEXUS AI RAG pipeline.\n\n"

            "The RAG system successfully "
            "received the provided context "
            "and user query."

        )