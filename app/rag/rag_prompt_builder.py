from typing import Any


class RAGPromptBuilder:
    """
    Builds professional prompts for the ANRO AI
    Retrieval-Augmented Generation (RAG) pipeline.

    The prompt instructs the language model to:

    - Answer only from retrieved context.
    - Avoid hallucinating information.
    - Clearly state when information is unavailable.
    - Use source references when possible.
    - Provide concise and useful answers.
    """

    def __init__(
        self,
        system_name: str = "ANRO AI",
    ):
        """
        Initialize the RAG prompt builder.
        """

        self.system_name = (
            system_name.strip()
            if system_name
            else "ANRO AI"
        )

    # ========================================================
    # BUILD SYSTEM PROMPT
    # ========================================================

    def build_system_prompt(
        self,
    ) -> str:
        """
        Build the main system instruction
        for the RAG language model.
        """

        return f"""
You are {self.system_name}, an intelligent
Document Intelligence and Retrieval-Augmented
Generation (RAG) assistant.

Your job is to answer the user's questions
using the provided document context.

IMPORTANT RULES:

1. Use the provided document context as
   the primary source of information.

2. Do not invent facts that are not present
   in the provided context.

3. If the answer is clearly available in the
   context, answer directly and confidently.

4. If the context does not contain enough
   information to answer the question, clearly
   say that the available documents do not
   provide enough information.

5. Do not claim that information is missing
   if the context actually contains the answer.

6. Do not mention internal implementation
   details such as embeddings, vector databases,
   retrieval distances, or prompt construction
   unless the user explicitly asks about them.

7. Keep answers clear, professional, and useful.

8. When source information is available,
   mention the relevant source number.

9. Do not repeat the same information unnecessarily.

10. Never fabricate citations or source references.

Your response should directly answer the
user's question based on the available context.
""".strip()

    # ========================================================
    # BUILD USER PROMPT
    # ========================================================

    def build_user_prompt(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Build the user prompt containing the
        original question and retrieved context.
        """

        question = (
            question.strip()
            if question
            else ""
        )

        context = (
            context.strip()
            if context
            else ""
        )

        if not question:

            raise ValueError(
                "Question cannot be empty."
            )

        # ====================================================
        # NO CONTEXT
        # ====================================================

        if not context:

            return f"""
User Question:

{question}

Document Context:

No relevant document context was found.

Instructions:

Answer the question only if it can be answered
reliably without document context.

If the question requires information from the
documents, clearly explain that no relevant
document information is currently available.
""".strip()

        # ====================================================
        # CONTEXT AVAILABLE
        # ====================================================

        return f"""
User Question:

{question}

Retrieved Document Context:

{context}

Instructions:

Answer the user's question using the retrieved
document context above.

Use only information supported by the context.

If the context contains the answer, provide a
direct and clear response.

If the context only partially answers the question,
explain what is known and what is not available.

If the context does not contain enough information,
say so clearly instead of inventing information.

When appropriate, reference the relevant source
using the source number provided in the context.
""".strip()

    # ========================================================
    # BUILD COMPLETE PROMPT
    # ========================================================

    def build_prompt(
        self,
        question: str,
        context: str,
    ) -> dict[str, str]:
        """
        Build the complete RAG prompt.

        Returns:
            Dictionary containing:
            - system_prompt
            - user_prompt
        """

        system_prompt = (
            self.build_system_prompt()
        )

        user_prompt = (
            self.build_user_prompt(
                question=question,
                context=context,
            )
        )

        return {
            "system_prompt":
                system_prompt,

            "user_prompt":
                user_prompt,
        }

    # ========================================================
    # BUILD CHAT MESSAGES
    # ========================================================

    def build_messages(
        self,
        question: str,
        context: str,
    ) -> list[dict[str, str]]:
        """
        Build messages compatible with
        OpenAI-style chat completion APIs
        and local Ollama-compatible models.
        """

        prompts = (
            self.build_prompt(
                question=question,
                context=context,
            )
        )

        return [

            {
                "role": "system",

                "content":
                    prompts[
                        "system_prompt"
                    ],
            },

            {
                "role": "user",

                "content":
                    prompts[
                        "user_prompt"
                    ],
            },

        ]

    # ========================================================
    # GET PROMPT STATISTICS
    # ========================================================

    def get_prompt_statistics(
        self,
        question: str,
        context: str,
    ) -> dict[str, Any]:
        """
        Return useful statistics about
        the generated RAG prompt.
        """

        prompts = (
            self.build_prompt(
                question=question,
                context=context,
            )
        )

        system_prompt = (
            prompts[
                "system_prompt"
            ]
        )

        user_prompt = (
            prompts[
                "user_prompt"
            ]
        )

        return {

            "question_characters":
                len(question),

            "context_characters":
                len(context),

            "system_prompt_characters":
                len(system_prompt),

            "user_prompt_characters":
                len(user_prompt),

            "total_prompt_characters":
                (
                    len(system_prompt)
                    + len(user_prompt)
                ),

            "context_available":
                bool(
                    context.strip()
                ),

        }