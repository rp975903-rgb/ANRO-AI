from app.ai.llm.local_llm import LocalLLM

from app.rag.rag_service import (
    RAGService
)

from app.interfaces.cli_chat import (
    CLIChat
)


def main():

    print()
    print("=" * 70)
    print("🧠 NEXUS AI CLI CHAT TEST")
    print("=" * 70)

    # ========================================================
    # INITIALIZE LOCAL LLM
    # ========================================================

    print()
    print("🤖 Initializing Local LLM...")

    llm = LocalLLM()

    print(
        f"✅ LLM Ready: {llm.model_name}"
    )

    # ========================================================
    # INITIALIZE RAG SERVICE
    # ========================================================

    print()
    print("🧠 Initializing RAG Service...")

    rag_service = RAGService(

        llm=llm,

        conversation_id=(
            "cli_test_conversation"
        ),

        top_k=3,

        max_context_length=5000

    )

    print(
        "✅ RAG Service Ready"
    )

    # ========================================================
    # INITIALIZE CLI CHAT
    # ========================================================

    print()
    print("💬 Starting CLI Chat...")

    chat = CLIChat(

        rag_service=rag_service

    )

    # ========================================================
    # START CHAT
    # ========================================================

    chat.start()


if __name__ == "__main__":

    main()