from .retrieval_service import (
    RetrievalService
)
from app.rag.rag_context_builder import (
    RAGContextBuilder
)
from ..ai.llm.base_llm import (
    BaseLLM
)

from .retrieval_analyzer import (
    RetrievalAnalyzer
)

from .citation_formatter import (
    CitationFormatter
)

from ..ai.conversation_memory import (
    ConversationMemory
)

from .query_rewriter import (
    QueryRewriter
)


class RAGService:
    """
    Main Retrieval-Augmented Generation service.

    Complete pipeline:

    User Question
        ↓
    Conversation Memory
        ↓
    Query Rewriting
        ↓
    Document Retrieval
        ↓
    Retrieval Analysis
        ↓
    Context Building
        ↓
    Prompt Construction
        ↓
    LLM Generation
        ↓
    Source Citations
        ↓
    Update Conversation Memory
        ↓
    Final Response
    """

    def __init__(
        self,
        llm: BaseLLM,
        conversation_id: str = "default_conversation",
        top_k: int = 3,
        max_context_length: int = 5000
    ):
        """
        Initialize RAG Service.
        """

        # ==================================================
        # VALIDATE LLM
        # ==================================================

        if llm is None:
            raise ValueError(
                "LLM instance cannot be None."
            )

        # ==================================================
        # VALIDATE CONVERSATION ID
        # ==================================================

        if not isinstance(
            conversation_id,
            str
        ):
            raise TypeError(
                "Conversation ID must be a string."
            )

        conversation_id = (
            conversation_id.strip()
        )

        if not conversation_id:
            raise ValueError(
                "Conversation ID cannot be empty."
            )

        # ==================================================
        # VALIDATE TOP K
        # ==================================================

        if not isinstance(
            top_k,
            int
        ):
            raise TypeError(
                "top_k must be an integer."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        # ==================================================
        # VALIDATE CONTEXT LENGTH
        # ==================================================

        if not isinstance(
            max_context_length,
            int
        ):
            raise TypeError(
                "max_context_length must be an integer."
            )

        if max_context_length <= 0:
            raise ValueError(
                "max_context_length must be greater than zero."
            )

        # ==================================================
        # STORE CONFIGURATION
        # ==================================================

        self.llm = llm

        self.conversation_id = (
            conversation_id
        )

        self.top_k = top_k

        self.max_context_length = (
            max_context_length
        )

        # ==================================================
        # QUERY REWRITER
        # ==================================================

        self.query_rewriter = (
            QueryRewriter(
                max_history_messages=6
            )
        )

        # ==================================================
        # RETRIEVAL SERVICE
        # ==================================================

        self.retrieval_service = (
            RetrievalService(
                top_k=top_k
            )
        )

        # ==================================================
        # CONTEXT BUILDER
        # ==================================================

        self.context_builder = (
            RAGContextBuilder(
                max_context_length=(
                    max_context_length
                )
            )
        )

        # ==================================================
        # RETRIEVAL ANALYZER
        # ==================================================

        self.retrieval_analyzer = (
            RetrievalAnalyzer()
        )

        # ==================================================
        # CITATION FORMATTER
        # ==================================================

        self.citation_formatter = (
            CitationFormatter()
        )

        # ==================================================
        # CONVERSATION MEMORY
        # ==================================================

        self.memory = (
            ConversationMemory(
                conversation_id=(
                    self.conversation_id
                ),
                max_messages=10
            )
        )

    # ======================================================
    # ASK QUESTION
    # ======================================================

    def ask(
        self,
        question: str,
        document_id: str | None = None
    ) -> dict:
        """
        Execute complete RAG pipeline.
        """

        # ==================================================
        # STEP 1: VALIDATE QUESTION
        # ==================================================

        if not isinstance(
            question,
            str
        ):
            raise TypeError(
                "Question must be a string."
            )

        question = (
            question.strip()
        )

        if not question:
            raise ValueError(
                "Question cannot be empty."
            )

        # ==================================================
        # STEP 2: VALIDATE DOCUMENT ID
        # ==================================================

        if document_id is not None:

            if not isinstance(
                document_id,
                str
            ):
                raise TypeError(
                    "document_id must be a string."
                )

            document_id = (
                document_id.strip()
            )

            if not document_id:
                document_id = None

        # ==================================================
        # STEP 3: GET CONVERSATION HISTORY
        # ==================================================

        conversation_history = (
            self.memory.get_raw_messages()
        )

        if conversation_history is None:
            conversation_history = []

        # ==================================================
        # STEP 4: REWRITE QUERY
        # ==================================================

        try:

            rewritten_query = (
                self.query_rewriter.rewrite(
                    question,
                    conversation_history
                )
            )

        except Exception:

            rewritten_query = question

        if not rewritten_query:
            rewritten_query = question

        rewritten_query = str(
            rewritten_query
        ).strip()

        # ==================================================
        # STEP 5: RETRIEVE DOCUMENTS
        # ==================================================

        try:

            retrieval_results = (
                self.retrieval_service.search(

                    query=(
                        rewritten_query
                    ),

                    top_k=(
                        self.top_k
                    ),

                    document_id=(
                        document_id
                    )

                )
            )

        except Exception as error:

            raise RuntimeError(
                "Document retrieval failed. "
                f"Error: {error}"
            ) from error

        if retrieval_results is None:
            retrieval_results = []

        # ==================================================
        # STEP 6: ANALYZE RETRIEVAL
        # ==================================================

        try:

            analysis = (
                self.retrieval_analyzer.analyze(
                    retrieval_results
                )
            )

        except Exception as error:

            analysis = {
                "success": False,
                "error": str(error)
            }

        # ==================================================
        # STEP 7: BUILD CONTEXT
        # ==================================================

        try:

            context = (
                self.context_builder.build_context(
                    retrieval_results
                )
            )

        except Exception as error:

            raise RuntimeError(
                "Failed to build document context. "
                f"Error: {error}"
            ) from error

        if context is None:
            context = ""

        context = str(
            context
        )

        # ==================================================
        # STEP 8: BUILD RAG PROMPT
        # ==================================================

        prompt = (
            self._build_prompt(

                question=(
                    question
                ),

                context=(
                    context
                ),

                conversation_history=(
                    conversation_history
                ),

                rewritten_query=(
                    rewritten_query
                ),

                document_id=(
                    document_id
                )

            )
        )

        # ==================================================
        # STEP 9: GENERATE ANSWER
        # ==================================================

        try:

            answer = (
                self.llm.generate(
                    prompt
                )
            )

        except Exception as error:

            raise RuntimeError(
                "Failed to generate RAG answer. "
                f"Error: {error}"
            ) from error

        if answer is None:
            raise RuntimeError(
                "LLM returned None answer."
            )

        answer = str(
            answer
        ).strip()

        if not answer:
            raise RuntimeError(
                "LLM returned empty answer."
            )

        # ==================================================
        # STEP 10: FORMAT CITATIONS
        # ==================================================

        citations = (
            self._format_citations(
                retrieval_results
            )
        )

        # ========================================================
        # STEP 11 — UPDATE CONVERSATION MEMORY
        # ========================================================

        try:
            self.memory.add_user_message(
                question
            )

            self.memory.add_assistant_message(
                answer
            )

        except Exception as error:
            raise RuntimeError(
                "Failed to update conversation memory. "
                f"Error: {error}"
            ) from error

        # ==================================================
        # STEP 12: FINAL RESPONSE
        # ==================================================

        return {
            "success": True,
            "conversation_id": (
                self.conversation_id
            ),
            "document_id": (
                document_id
            ),
            "question": (
                question
            ),
            "rewritten_query": (
                rewritten_query
            ),
            "answer": (
                answer
            ),
            "citations": (
                citations
            ),
            "analysis": (
                analysis
            ),
            "memory_size": (
                self.get_memory_size()
            )
        }

    # ======================================================
    # FORMAT CITATIONS
    # ======================================================

    def _format_citations(
        self,
        retrieval_results
    ):
        """
        Format citations safely.

        Supports:

        1. format_sources()
        2. format()

        If neither method exists,
        returns an empty list.
        """

        if retrieval_results is None:
            retrieval_results = []

        # --------------------------------------------------
        # TRY format_sources()
        # --------------------------------------------------

        if hasattr(
            self.citation_formatter,
            "format_sources"
        ):

            try:

                return (
                    self.citation_formatter.format_sources(
                        retrieval_results
                    )
                )

            except Exception:

                pass

        # --------------------------------------------------
        # TRY format()
        # --------------------------------------------------

        if hasattr(
            self.citation_formatter,
            "format"
        ):

            try:

                return (
                    self.citation_formatter.format(
                        retrieval_results
                    )
                )

            except Exception:

                pass

        # --------------------------------------------------
        # FALLBACK
        # --------------------------------------------------

        return []

    # ======================================================
    # BUILD RAG PROMPT
    # ======================================================

    def _build_prompt(
        self,
        question: str,
        context: str,
        conversation_history: list[dict],
        rewritten_query: str,
        document_id: str | None = None
    ) -> str:
        """
        Build strict grounded RAG prompt.
        """

        # ==================================================
        # FORMAT HISTORY
        # ==================================================

        history_text = (
            self._format_conversation_history(
                conversation_history
            )
        )

        # ==================================================
        # EMPTY CONTEXT
        # ==================================================

        if not context.strip():

            context = (
                "No relevant document context "
                "was retrieved."
            )

        # ==================================================
        # SELECTED DOCUMENT
        # ==================================================

        selected_document = (

            document_id

            if document_id

            else "ALL DOCUMENTS"

        )

        # ==================================================
        # FINAL PROMPT
        # ==================================================

        return f"""
You are NEXUS AI, an intelligent
document intelligence assistant.

Your primary task is to answer the user's
question using ONLY the information contained
in the provided DOCUMENT CONTEXT.

==================================================
STRICT GROUNDING RULES
==================================================

1. Use only the provided DOCUMENT CONTEXT.

2. Do NOT use outside knowledge.

3. Do NOT invent facts, names, numbers,
   explanations, or conclusions.

4. Do NOT guess the answer.

5. If the answer is not clearly available,
   say:

"The information was not found clearly
in the provided documents."

6. If only partial information is available,
   provide only the supported information.

7. Clearly label any document-based inference
   with:

"Inference:"

8. Do not present an inference as a confirmed fact.

9. When asked for a list, return only items
   explicitly supported by the documents.

10. Keep the answer concise and factual.

==================================================
CONVERSATION CONTEXT RULES
==================================================

Conversation history may be used only to
understand references such as:

- it
- this
- that
- they
- previous question
- previous topic

Conversation history is NOT factual evidence.

All factual answers must be grounded in the
DOCUMENT CONTEXT.

==================================================
CONVERSATION ID
==================================================

{self.conversation_id}

==================================================
SELECTED DOCUMENT ID
==================================================

{selected_document}

==================================================
CONVERSATION HISTORY
==================================================

{history_text}

==================================================
ORIGINAL USER QUESTION
==================================================

{question}

==================================================
REWRITTEN SEARCH QUERY
==================================================

{rewritten_query}

==================================================
DOCUMENT CONTEXT
==================================================

{context}

==================================================
FINAL ANSWERING INSTRUCTIONS
==================================================

Answer the ORIGINAL USER QUESTION directly.

If the information is clearly present:
Give the answer directly.

If the information is partially present:
Give only the supported information and mention
what is missing.

If the information is not present:
Do not guess.

Say:

"The information was not found clearly
in the provided documents."

Keep the answer concise and factual.

==================================================
FINAL ANSWER
==================================================
"""

    # ======================================================
    # FORMAT CONVERSATION HISTORY
    # ======================================================

    def _format_conversation_history(
        self,
        conversation_history: list[dict]
    ) -> str:
        """
        Convert conversation history
        into readable text.
        """

        if not conversation_history:

            return (
                "No previous conversation."
            )

        formatted_messages = []

        for message in conversation_history:

            if not isinstance(
                message,
                dict
            ):
                continue

            role = (
                message.get(
                    "role",
                    "unknown"
                )
            )

            content = (
                message.get(
                    "content",
                    ""
                )
            )

            if not content:
                continue

            formatted_messages.append(
                f"{str(role).upper()}: "
                f"{str(content)}"
            )

        if not formatted_messages:

            return (
                "No previous conversation."
            )

        return "\n".join(
            formatted_messages
        )

    # ======================================================
    # GET CONVERSATION ID
    # ======================================================

    def get_conversation_id(
        self
    ) -> str:

        return (
            self.conversation_id
        )

    # ======================================================
    # GET MEMORY
    # ======================================================

    def get_memory(
        self
    ):

        messages = (
            self.memory.get_raw_messages()
        )

        if messages is None:
            return []

        return messages

    # ======================================================
    # GET MEMORY SIZE
    # ======================================================

    def get_memory_size(
        self
    ) -> int:

        messages = (
            self.memory.get_raw_messages()
        )

        if messages is None:
            return 0

        return len(
            messages
        )

    # ======================================================
    # CLEAR CONVERSATION
    # ======================================================

    def clear_conversation(
        self
    ) -> bool:
        """
        Clear conversation memory.
        """

        try:

            self.memory.clear()

            return True

        except Exception:

            return False